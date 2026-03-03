import unittest
import time
import importlib.util
import sys

# Importar dinámicamente el módulo con nombre que comienza con número

spec = importlib.util.spec_from_file_location("module_2_1", "2_1_a_refactorizar.py")
#spec = importlib.util.spec_from_file_location("module_2_1", "2_1_a_refactorizar_refactorizado.py")

module_2_1 = importlib.util.module_from_spec(spec)  # pyright: ignore[reportArgumentType]
sys.modules["module_2_1"] = module_2_1
spec.loader.exec_module(module_2_1)                 # pyright: ignore[reportOptionalMemberAccess]

find_duplicates_and_count = module_2_1.find_duplicates_and_count


class TestPerformanceWithLargeList(unittest.TestCase):
    """Tests para medir el rendimiento con listas grandes."""
    
    def setUp(self):
        """Configura los datos de prueba."""
        # Crear una lista de 10,000 elementos con algunos duplicados
        self.large_list = list(range(5000)) * 2  # 5000 números repetidos 2 veces = 10,000 elementos

        
    # def test_find_duplicates_execution_time(self):
    #     """Mide el tiempo de ejecución de find_duplicates_and_count con 10,000 elementos."""
    #     start_time = time.time()
    #     result = find_duplicates_and_count(self.large_list)
    #     end_time = time.time()
        
    #     execution_time = end_time - start_time
        
    #     # Mostrar información del rendimiento
    #     print(f"\n--- Resultados de Rendimiento ---")
    #     print(f"Tamaño de lista: {len(self.large_list)} elementos")
    #     print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
    #     print(f"Elementos únicos duplicados encontrados: {len(result)}")
        
    #     # Verificar que la función retorna un diccionario
    #     self.assertIsInstance(result, dict)
        
    #     # Verificar que encontró duplicados (todos los 5000 números aparecen 2 veces)
    #     self.assertEqual(len(result), 5000)
        
    #     # Verificar que cada valor es 2 (cada número aparece exactamente 2 veces)
    #     for count in result.values():
    #         self.assertEqual(count, 2)
        
    #     # Advertencia si el tiempo es muy largo (más de 5 segundos)
    #     if execution_time > 5:
    #         print(f"⚠️ ADVERTENCIA: Tiempo de ejecución muy alto ({execution_time:.4f}s)")
            
    def test_find_duplicates_with_various_sizes(self):
        """Prueba el rendimiento con varios tamaños de lista."""
        sizes = [100000]
      
        print(f"\n--- Pruebas de Rendimiento con Diferentes Tamaños ---")
      
        for size in sizes:
            test_list = list(range(size // 2)) * 2  # Crear lista con duplicados
          
            start_time = time.time()
            result = find_duplicates_and_count(test_list)
            end_time = time.time()
          
            execution_time = end_time - start_time
          
            print(f"Tamaño: {size} elementos | Tiempo: {execution_time:.4f} segundos")
          
            # Validar que la función retorna una lista
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
