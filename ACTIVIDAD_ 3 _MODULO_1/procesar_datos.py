def procesar_datos(numeros):
    """
    Procesa una lista de números: duplica los pares, triplica los impares.
    
    Mejoras:
    1. Corrección de sintaxis: '@' cambiado por '0' y 'mum' por 'num'.
    2. Legibilidad: Nombres de variables más semánticos.
    3. Eficiencia: Uso de generadores si fuera necesario (opcional).
    """
    return [num * 2 if num % 2 == 0 else num * 3 for num in numeros]

def procesar_datos_pro(numeros):
    """
    Versión optimizada usando operadores de bits para máximo rendimiento.
    """
    # num % 2 == 0 es equivalente a (num & 1) == 0 pero más lento
    return [num * (2 if not (num & 1) else 3) for num in numeros]