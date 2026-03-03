import csv
import json
from typing import Generator, Dict, Tuple, Optional, Any
from collections import defaultdict
import os
import tempfile
from pathlib import Path


def csv_reader_streaming(csv_file_path: str, chunk_size: int = 10000) -> Generator[list, None, None]:
    """
    Lee un archivo CSV en chunks para procesamiento eficiente de memoria.
    
    Args:
        csv_file_path: Ruta del archivo CSV
        chunk_size: Número de filas por chunk
        
    Yields:
        Listas de diccionarios (filas del CSV)
        
    Complejidad: O(n) - una sola pasada al archivo
    Espacio: O(chunk_size)
    """
    chunk = []
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                chunk.append(row)
                if len(chunk) >= chunk_size:
                    yield chunk
                    chunk = []
            
            # Yield el último chunk si no está vacío
            if chunk:
                yield chunk
                
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo CSV no encontrado: {csv_file_path}")
    except Exception as e:
        raise Exception(f"Error al leer CSV: {str(e)}")


def _make_hashable(obj: Any) -> Any:
    """
    Convierte un objeto no hashable a una versión hashable.
    
    Soporta: listas, diccionarios, sets y otros tipos no hashables.
    Complejidad: O(n) donde n es el tamaño del objeto.
    """
    if isinstance(obj, dict):
        return tuple(sorted((k, _make_hashable(v)) for k, v in obj.items()))
    elif isinstance(obj, list):
        return tuple(_make_hashable(item) for item in obj)
    elif isinstance(obj, set):
        return frozenset(_make_hashable(item) for item in obj)
    elif isinstance(obj, tuple):
        return tuple(_make_hashable(item) for item in obj)
    else:
        try:
            hash(obj)
            return obj
        except TypeError:
            return json.dumps(obj, sort_keys=True, default=str)


def find_duplicates_streaming(csv_file_path: str, 
                             column: Optional[str] = None,
                             use_disk_cache: bool = False) -> Generator[Tuple[Any, int], None, None]:
    """
    Encuentra duplicados en un archivo CSV sin cargar todo en memoria.
    Procesamiento en streaming con soporte para archivos muy grandes.
    
    Args:
        csv_file_path: Ruta del archivo CSV
        column: Columna específica a procesar (None = procesar filas completas)
        use_disk_cache: Usar archivo temporal en disco para conteos (útil para mucha memoria)
        
    Yields:
        Tuplas (elemento, cantidad) para cada duplicado encontrado
        
    Complejidad: O(n) - una sola pasada al archivo
    Espacio: O(k) donde k es el número de elementos únicos en memoria
    """
    
    count_dict = {}
    hashable_to_original = {}
    temp_file = None
    
    try:
        # Procesar el CSV en chunks
        for chunk in csv_reader_streaming(csv_file_path):
            for row in chunk:
                # Extraer elemento a procesar
                if column:
                    element = row.get(column, '')
                else:
                    element = row
                
                # Convertir a hashable
                hashable_element = _make_hashable(element)
                
                # Guardar versión original
                if hashable_element not in hashable_to_original:
                    hashable_to_original[hashable_element] = element
                
                # Contar ocurrencias
                count_dict[hashable_element] = count_dict.get(hashable_element, 0) + 1
        
        # Retornar duplicados encontrados
        for hashable_elem, count in count_dict.items():
            if count > 1:
                yield (hashable_to_original[hashable_elem], count)
    
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)


def find_duplicates_streaming_with_disk(csv_file_path: str,
                                       column: Optional[str] = None,
                                       batch_size: int = 50000,
                                       memory_threshold_mb: int = 500) -> Generator[Tuple[Any, int], None, None]:
    """
    Versión mejorada que usa disco temporal cuando la memoria se aproxima al límite.
    Ideal para archivos enormes (millones de filas).
    
    Args:
        csv_file_path: Ruta del archivo CSV
        column: Columna específica a procesar
        batch_size: Filas a procesar antes de verificar memoria
        memory_threshold_mb: Umbral de memoria antes de usar disco
        
    Yields:
        Tuplas (elemento, cantidad) para cada duplicado
        
    Complejidad: O(n) tiempo; O(k) memoria con desborde a disco
    """
    import sys
    
    count_dict = {}
    hashable_to_original = {}
    temp_dir = None
    batch_file_counter = 0
    processed_rows = 0
    
    try:
        temp_dir = tempfile.mkdtemp(prefix='csv_duplicates_')
        
        # Procesar archivo
        for chunk in csv_reader_streaming(csv_file_path, chunk_size=batch_size):
            for row in chunk:
                # Extraer elemento
                if column:
                    element = row.get(column, '')
                else:
                    element = row
                
                # Convertir a hashable
                hashable_element = _make_hashable(element)
                
                # Guardar original
                if hashable_element not in hashable_to_original:
                    hashable_to_original[hashable_element] = element
                
                # Contar
                count_dict[hashable_element] = count_dict.get(hashable_element, 0) + 1
                processed_rows += 1
            
            # Verificar memoria cada batch
            memory_usage = sys.getsizeof(count_dict) / (1024 * 1024)
            if memory_usage > memory_threshold_mb:
                # Guardar batch actual a disco y limpiar memoria
                batch_file = os.path.join(temp_dir, f'batch_{batch_file_counter}.json')
                with open(batch_file, 'w') as f:
                    json.dump({str(k): v for k, v in count_dict.items()}, f)
                count_dict.clear()
                batch_file_counter += 1
        
        # Retornar todos los duplicados
        for hashable_elem, count in count_dict.items():
            if count > 1:
                yield (hashable_to_original[hashable_elem], count)
        
        # Procesar archivos temporales si existen
        if batch_file_counter > 0:
            final_counts = defaultdict(int)
            for i in range(batch_file_counter):
                batch_file = os.path.join(temp_dir, f'batch_{i}.json')
                if os.path.exists(batch_file):
                    with open(batch_file, 'r') as f:
                        batch_data = json.load(f)
                        for key_str, count in batch_data.items():
                            final_counts[key_str] += count
            
            # Convertir strings de vuelta a valores originales
            for key_str, count in final_counts.items():
                if count > 1:
                    # Recuperar valor original
                    try:
                        original_value = json.loads(key_str)
                        yield (original_value, count)
                    except:
                        yield (key_str, count)
    
    finally:
        # Limpiar archivos temporales
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)


def create_sample_csv(file_path: str, num_rows: int = 10000, num_duplicates: int = 100):
    """
    Crea un archivo CSV de ejemplo para testing.
    
    Args:
        file_path: Ruta donde guardar el CSV
        num_rows: Número de filas a generar
        num_duplicates: Número de valores únicos que se duplicarán
    """
    import random
    
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'value', 'category'])
        writer.writeheader()
        
        # Crear valores duplicados
        duplicate_values = [f'name_{i}' for i in range(num_duplicates)]
        
        for i in range(num_rows):
            row = {
                'id': i,
                'name': random.choice(duplicate_values),
                'value': random.randint(1, 1000),
                'category': random.choice(['A', 'B', 'C', 'D'])
            }
            writer.writerow(row)


def print_duplicates_summary(csv_file_path: str, column: Optional[str] = None, limit: int = 10):
    """
    Imprime un resumen de duplicados encontrados.
    
    Args:
        csv_file_path: Ruta del archivo CSV
        column: Columna a procesar
        limit: Número máximo de resultados a mostrar
    """
    print(f"\n=== Análisis de Duplicados ===")
    print(f"Archivo: {csv_file_path}")
    print(f"Columna analizada: {column or 'fila completa'}\n")
    
    duplicates = []
    for element, count in find_duplicates_streaming(csv_file_path, column):
        duplicates.append((element, count))
    
    # Ordenar por cantidad descendente
    duplicates.sort(key=lambda x: x[1], reverse=True)
    
    total_duplicates = len(duplicates)
    total_duplicate_rows = sum(count - 1 for _, count in duplicates)
    
    print(f"Total de elementos duplicados: {total_duplicates}")
    print(f"Total de filas duplicadas: {total_duplicate_rows}")
    print(f"\nTop {min(limit, total_duplicates)} duplicados:")
    print("-" * 60)
    
    for element, count in duplicates[:limit]:
        element_str = str(element)[:50]
        print(f"  {element_str:<50} | Apariciones: {count}")
    
    if total_duplicates > limit:
        print(f"  ... y {total_duplicates - limit} más")
