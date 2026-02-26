import unittest
import time
import random
from MyLRUCache import LRUCache

class TestLRUPerformance(unittest.TestCase):
    def setUp(self):
        self.small_capacity = 100
        self.large_capacity = 100_000
        self.num_operations = 50_000 # Operaciones a medir

    def _measure_latency(self, capacity: int) -> float:
        cache = LRUCache(capacity)
        # 1. Llenar el caché para llegar al estado de "evicción" constante
        for i in range(capacity):
            cache.put(i, i)
        
        start_time = time.perf_counter()
        
        # 2. Realizar ráfaga de operaciones put/get aleatorias
        for i in range(self.num_operations):
            key = random.randint(0, capacity * 2)
            if i % 2 == 0:
                cache.put(key, i)
            else:
                cache.get(key)
                
        end_time = time.perf_counter()
        return (end_time - start_time) / self.num_operations

    def test_time_complexity_is_constant(self):
        """
        Compara la latencia promedio entre un caché pequeño y uno 1000x más grande.
        En O(1), la diferencia de tiempo debe ser mínima (ruido del sistema).
        """
        avg_latency_small = self._measure_latency(self.small_capacity)
        avg_latency_large = self._measure_latency(self.large_capacity)
        
        print(f"\nLatencia promedio (Capacidad {self.small_capacity}): {avg_latency_small:.8f}s")
        print(f"Latencia promedio (Capacidad {self.large_capacity}): {avg_latency_large:.8f}s")
        
        # Tolerancia: La latencia no debería dispararse proporcionalmente al tamaño.
        # Un aumento de 1000x en tamaño no debería duplicar el tiempo de ejecución.
        ratio = avg_latency_large / avg_latency_small
        
        self.assertLess(ratio, 2.0, f"La latencia creció demasiado (Ratio: {ratio:.2f}). No parece O(1).")

if __name__ == '__main__':
    unittest.main()