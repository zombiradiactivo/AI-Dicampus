import json


def _make_hashable(obj):
    """
    Convierte un objeto no hashable a una versión hashable.
    
    Soporta: listas, diccionarios, sets y otros tipos no hashables.
    Complejidad: O(n) donde n es el tamaño del objeto.
    """
    if isinstance(obj, dict):
        # Convertir diccionario a tupla de items ordenados
        return tuple(sorted((k, _make_hashable(v)) for k, v in obj.items()))
    elif isinstance(obj, list):
        # Convertir lista a tupla
        return tuple(_make_hashable(item) for item in obj)
    elif isinstance(obj, set):
        # Convertir set a frozenset
        return frozenset(_make_hashable(item) for item in obj)
    elif isinstance(obj, tuple):
        # Tuplas que contienen no-hashables
        return tuple(_make_hashable(item) for item in obj)
    else:
        # Retornar el objeto original si ya es hashable
        try:
            hash(obj)
            return obj
        except TypeError:
            # Si no es hashable, convertir a string JSON como último recurso
            return json.dumps(obj, sort_keys=True, default=str)


def find_duplicates_and_count(data: list):
    """
    Encuentra elementos duplicados y cuántas veces aparecen.
    Maneja elementos hashables y no hashables (listas, dicts, etc).
    
    Retorna: Lista de tuplas (elemento, cantidad) para cada duplicado.
    
    Complejidad: O(n) - Una sola pasada por la lista.
    Espacio: O(k) donde k es el número de elementos únicos.
    """
    # Mapeo de versiones hashables a originales
    hashable_to_original = {}
    count_dict = {}
    
    for element in data:
        # Convertir a versión hashable si es necesario
        hashable_element = _make_hashable(element)
        
        # Guardar la versión original para usarla en el resultado
        if hashable_element not in hashable_to_original:
            hashable_to_original[hashable_element] = element
        
        # Contar ocurrencias
        count_dict[hashable_element] = count_dict.get(hashable_element, 0) + 1
    
    # Filtrar solo elementos que aparecen más de una vez
    # Retornar como lista de tuplas (elemento_original, count)
    result = [
        (hashable_to_original[hashable_elem], count) 
        for hashable_elem, count in count_dict.items() 
        if count > 1
    ]
    
    return result