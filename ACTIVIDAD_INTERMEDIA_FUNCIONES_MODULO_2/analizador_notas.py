def analizar_notas(alumnos: list[tuple[str, float]]):
    """
    Analiza una lista de alumnos y sus notas para obtener estadísticas básicas.

    Args:
        alumnos (list[tuple[str, float]]): Una lista de tuplas donde cada tupla 
            contiene el nombre del alumno (str) y su nota (float).

    Returns:
        dict[str, Optional[float | str]]: Un diccionario con la nota máxima, 
            mínima, media y el nombre del mejor alumno. Si la lista está vacía, 
            devuelve valores None o 0.
    """
    # 1. Manejo de lista vacía
    if not alumnos:
        return {
            "nota_maxima": None,
            "nota_minima": None,
            "nota_media": 0,
            "mejor_alumno": None
        }

    # 2. Extraer solo las notas para cálculos numéricos
    notas = [alumno[1] for alumno in alumnos]
    
    # 3. Cálculos
    nota_max = max(notas)
    nota_min = min(notas)
    nota_media = sum(notas) / len(notas)
    
    # 4. Encontrar al mejor alumno/a (el primero que coincida con la nota máxima)
    # Usamos el parámetro 'key' de max para comparar por la nota (índice 1 de la tupla)
    mejor_estudiante = max(alumnos, key=lambda x: x[1])[0]
    print(f"La nota maxima es: {nota_max} \nLa nota minima es: {nota_min}\nLa nota media es: {round(nota_media, 2)}\nEl alumno con mejor nota es: {mejor_estudiante}")

    return {
        "nota_maxima": nota_max,
        "nota_minima": nota_min,
        "nota_media": round(nota_media, 2), # Redondeado para que quede más limpio
        "mejor_alumno": mejor_estudiante
    }


estudiantes = [("Andres", 9.5), ("Luis", 8.0), ("Marta", 7.2)]
resultado = analizar_notas(estudiantes)
print(resultado)