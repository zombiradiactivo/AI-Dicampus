import unittest
from Cycle_Detection import tiene_ciclo

class TestDeteccionCiclos(unittest.TestCase):

    # def test_grafo_vacio(self):
    #     grafo = {}
    #     self.assertFalse(tiene_ciclo(grafo), "Un grafo vacío no debería tener ciclos")

    # def test_sin_ciclo(self):
    #     # 0 -> 1 -> 2
    #     grafo = {0: [1], 1: [2], 2: []}
    #     self.assertFalse(tiene_ciclo(grafo), "El grafo es lineal y acíclico")

    # def test_con_ciclo_simple(self):
    #     # 0 -> 1 -> 2 -> 0
    #     grafo = {0: [1], 1: [2], 2: [0]}
    #     self.assertTrue(tiene_ciclo(grafo), "Debería detectar el ciclo 0-1-2-0")

    # def test_ciclo_autocontrol(self):
    #     # 0 -> 0 (self-loop)
    #     grafo = {0: [0]}
    #     self.assertTrue(tiene_ciclo(grafo), "Debería detectar un nodo que se apunta a sí mismo")

    # def test_grafo_desconectado_con_ciclo(self):
    #     # Componente 1: 0 -> 1
    #     # Componente 2: 2 -> 3 -> 2
    #     grafo = {
    #         0: [1],
    #         1: [],
    #         2: [3],
    #         3: [2]
    #     }
    #     self.assertTrue(tiene_ciclo(grafo), "Debería detectar el ciclo en la segunda componente")

    def test_grafo_grande_acido(self):
        # Crear una cadena larga de 10,000 nodos sin ciclos
        grafo = {i: [i + 1] for i in range(9999)}
        grafo[9999] = []
        self.assertFalse(tiene_ciclo(grafo), "No debería fallar por recursión ni detectar ciclo")

if __name__ == '__main__':
    # Para ejecutar en un script: python nombre_del_archivo.py
    unittest.main(argv=['first-arg-is-ignored'], exit=False)