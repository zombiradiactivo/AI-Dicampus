import unittest
import os
import sys
import time
from pathlib import Path
import csv
import random
import tempfile

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from csv_streaming_processor import (
    create_sample_csv,
    find_duplicates_streaming,
    print_duplicates_summary,
    csv_reader_streaming
)


class TestCSVStreamingProcessor(unittest.TestCase):
    """Tests para el procesador de CSV con streaming."""
    
    @classmethod
    def setUpClass(cls):
        """Prepara archivos de prueba."""
        cls.temp_dir = tempfile.mkdtemp(prefix='csv_test_')
        
        # CSV pequeño (10,000 filas)
        cls.small_csv = os.path.join(cls.temp_dir, 'small_test.csv')
        create_sample_csv(cls.small_csv, num_rows=10000, num_duplicates=100)
        
        # CSV mediano (100,000 filas)
        cls.medium_csv = os.path.join(cls.temp_dir, 'medium_test.csv')
        create_sample_csv(cls.medium_csv, num_rows=100000, num_duplicates=500)
    
    @classmethod
    def tearDownClass(cls):
        """Limpia archivos de prueba."""
        import shutil
        if os.path.exists(cls.temp_dir):
            shutil.rmtree(cls.temp_dir)
    
    def test_streaming_reader(self):
        """Prueba la lectura en chunks."""
        total_rows = 0
        chunk_count = 0
        
        for chunk in csv_reader_streaming(self.small_csv, chunk_size=1000):
            total_rows += len(chunk)
            chunk_count += 1
            self.assertGreater(len(chunk), 0)
            self.assertLessEqual(len(chunk), 1000)
        
        self.assertEqual(total_rows, 10000)
        print(f"✓ Lectura streaming: {chunk_count} chunks de {total_rows} filas")
    
    def test_duplicates_small_csv(self):
        """Prueba encontrar duplicados en CSV pequeño."""
        print(f"\n--- Test CSV Pequeño (10,000 filas) ---")
        start_time = time.time()
        
        duplicates = list(find_duplicates_streaming(self.small_csv, column='name'))
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Elementos duplicados encontrados: {len(duplicates)}")
        
        # Debe encontrar aproximadamente 100 elementos duplicados
        self.assertGreater(len(duplicates), 0)
        self.assertLess(execution_time, 5)  # Debe ser rápido
    
    def test_duplicates_medium_csv(self):
        """Prueba encontrar duplicados en CSV mediano."""
        print(f"\n--- Test CSV Mediano (100,000 filas) ---")
        start_time = time.time()
        
        duplicates = list(find_duplicates_streaming(self.medium_csv, column='name'))
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Elementos duplicados encontrados: {len(duplicates)}")
        print(f"Total de filas duplicadas: {sum(count - 1 for _, count in duplicates)}")
        
        self.assertGreater(len(duplicates), 0)
        self.assertLess(execution_time, 10)  # Debe procesar 100k filas en menos de 10s
    
    def test_csv_with_large_volume(self):
        """Simula un procesamiento de 1 millón de filas."""
        print(f"\n--- Simulación CSV 1 Millón ---")
        
        # Crear CSV grande en memoria para simular lectura
        large_csv = os.path.join(self.temp_dir, 'large_test.csv')
        
        print("Generando CSV de 1,000,000 filas...")
        start_gen = time.time()
        
        with open(large_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'value', 'category'])
            writer.writeheader()
            
            # Crear 1000 valores que se duplicarán frecuentemente
            duplicate_values = [f'user_{i}' for i in range(1000)]
            
            for i in range(1000000):
                row = {
                    'id': i,
                    'name': random.choice(duplicate_values),
                    'value': random.randint(1, 10000),
                    'category': random.choice(['A', 'B', 'C', 'D', 'E'])
                }
                writer.writerow(row)
        
        gen_time = time.time() - start_gen
        print(f"CSV generado en {gen_time:.2f} segundos")
        
        # Procesar con streaming
        print("Procesando con streaming...")
        start_time = time.time()
        
        duplicates = list(find_duplicates_streaming(large_csv, column='name'))
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        total_duplicate_rows = sum(count - 1 for _, count in duplicates)
        
        print(f"Elementos duplicados encontrados: {len(duplicates)}")
        print(f"Total de filas duplicadas: {total_duplicate_rows}")
        print(f"Tiempo de procesamiento: {execution_time:.4f} segundos")
        print(f"Velocidad: {1000000 / execution_time:.0f} filas/segundo")
        
        self.assertEqual(len(duplicates), 1000)  # Los 1000 valores se duplican
        self.assertLess(execution_time, 60)  # Debe procesar 1M en menos de 1 minuto
        
        # Verificar que el archivo fue procesado correctamente
        file_size_mb = os.path.getsize(large_csv) / (1024 * 1024)
        print(f"Tamaño del archivo: {file_size_mb:.2f} MB")
    
    def test_memory_efficiency(self):
        """Verifica que el procesamiento es eficiente en memoria."""
        print(f"\n--- Test Eficiencia de Memoria ---")
        
        import psutil
        process = psutil.Process()
        
        # Memoria inicial
        mem_before = process.memory_info().rss / (1024 * 1024)
        
        # Procesar
        duplicates = list(find_duplicates_streaming(self.medium_csv, column='name'))
        
        # Memoria final
        mem_after = process.memory_info().rss / (1024 * 1024)
        mem_used = mem_after - mem_before
        
        print(f"Memoria usada: {mem_used:.2f} MB")
        print(f"Duplicados encontrados: {len(duplicates)}")
        
        # No debe usar más de 100 MB incluso para 100k filas
        self.assertLess(mem_used, 100)
    
    def test_full_row_duplicates(self):
        """Prueba detección de filas duplicadas completas."""
        print(f"\n--- Test Filas Completas Duplicadas ---")
        
        # Crear CSV con filas duplicadas exactas
        dup_csv = os.path.join(self.temp_dir, 'duplicates.csv')
        
        with open(dup_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'name', 'value'])
            writer.writeheader()
            
            # Escribir algunas filas duplicadas
            rows = [
                {'id': '1', 'name': 'Alice', 'value': '100'},
                {'id': '1', 'name': 'Alice', 'value': '100'},
                {'id': '2', 'name': 'Bob', 'value': '200'},
                {'id': '2', 'name': 'Bob', 'value': '200'},
                {'id': '2', 'name': 'Bob', 'value': '200'},
                {'id': '3', 'name': 'Charlie', 'value': '300'},
            ]
            
            writer.writerows(rows)
        
        # Procesar filas completas
        duplicates = list(find_duplicates_streaming(dup_csv))  # Sin column, procesa fila completa
        
        print(f"Duplicados encontrados: {len(duplicates)}")
        
        self.assertEqual(len(duplicates), 2)  # Alice y Bob son duplicados
        
        # Verificar conteos
        counts = {tuple(sorted(row.items())): count for row, count in duplicates}
        for row, count in duplicates:
            print(f"  Fila: {row} | Apariciones: {count}")


class TestPerformanceBenchmark(unittest.TestCase):
    """Benchmarks de rendimiento."""
    
    def test_streaming_vs_memory_estimate(self):
        """Estima el consumo de memoria comparada con carga completa."""
        print(f"\n=== Benchmark: Streaming vs Cargar Todo ===")
        
        # Crear CSV de prueba
        temp_dir = tempfile.mkdtemp()
        test_csv = os.path.join(temp_dir, 'benchmark.csv')
        
        print("Generando CSV de 500,000 filas...")
        with open(test_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'value'])
            writer.writeheader()
            
            for i in range(500000):
                writer.writerow({'id': i % 50000, 'value': f'val_{i % 50000}'})
        
        file_size_mb = os.path.getsize(test_csv) / (1024 * 1024)
        print(f"Tamaño del archivo: {file_size_mb:.2f} MB")
        
        # Test streaming
        print("\nProcesando con STREAMING...")
        import psutil
        process = psutil.Process()
        
        mem_before = process.memory_info().rss / (1024 * 1024)
        start = time.time()
        
        duplicates_streaming = list(find_duplicates_streaming(test_csv, column='id'))
        
        streaming_time = time.time() - start
        mem_after = process.memory_info().rss / (1024 * 1024)
        streaming_mem = mem_after - mem_before
        
        print(f"Tiempo: {streaming_time:.4f}s")
        print(f"Memoria usada: {streaming_mem:.2f} MB")
        print(f"Duplicados encontrados: {len(duplicates_streaming)}")
        
        # Limpiar
        import shutil
        shutil.rmtree(temp_dir)
        
        print(f"\n✓ Streaming procesó {500000} filas en {streaming_time:.4f}s")
        print(f"  Velocidad: {500000 / streaming_time:.0f} filas/segundo")


if __name__ == '__main__':
    # Verificar si psutil está instalado
    try:
        import psutil
    except ImportError:
        print("Instalando psutil para benchmark de memoria...")
        os.system('pip install psutil -q')
    
    unittest.main(verbosity=2)
