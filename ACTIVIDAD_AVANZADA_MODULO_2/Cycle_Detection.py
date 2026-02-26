import sys

def tiene_ciclo(grafo: dict[int, list[int]]) -> bool:
    # Aumentar límite de recursión para grafos profundos
    sys.setrecursionlimit(20000)
    
    # 0: Blanco, 1: Gris, 2: Negro
    colores = {nodo: 0 for nodo in grafo}
    
    def dfs(u):
        colores[u] = 1  # Marcamos como GRIS (visitando)
        
        for v in grafo.get(u, []):
            if colores.get(v, 0) == 1:
                return True  # ¡Ciclo detectado!
            if colores.get(v, 0) == 0:
                if dfs(v):
                    return True
        
        colores[u] = 2  # Marcamos como NEGRO (procesado)
        return False

    for nodo in grafo:
        if colores[nodo] == 0:
            if dfs(nodo):
                return True
                
    return False

# Ejemplo de uso:
# grafo = {0: [1], 1: [2], 2: [0]} -> True