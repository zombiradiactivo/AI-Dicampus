import unittest
import importlib.util
import sys

# Importar el módulo refactorizado
spec = importlib.util.spec_from_file_location(
    "module_refactorizado", 
    "2_1_a_refactorizar_refactorizado.py"
)
module_refactorizado = importlib.util.module_from_spec(spec)    # pyright: ignore[reportArgumentType]
sys.modules["module_refactorizado"] = module_refactorizado
spec.loader.exec_module(module_refactorizado)                   # pyright: ignore[reportOptionalMemberAccess]

find_duplicates_and_count = module_refactorizado.find_duplicates_and_count


class TestNonHashableElements(unittest.TestCase):
    """Tests para verificar manejo de elementos no hashables."""
    
    def test_with_lists(self):
        """Prueba con listas como elementos."""
        data = [
            [1, 2, 3],
            [1, 2, 3],
            [4, 5, 6],
            [4, 5, 6],
            [4, 5, 6],
        ]
        result = find_duplicates_and_count(data)
        
        # Convertir resultado a diccionario para verificación
        result_dict = {tuple(item[0]): item[1] for item in result}
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result_dict[(1, 2, 3)], 2)
        self.assertEqual(result_dict[(4, 5, 6)], 3)
        print("✓ Test con listas pasado")
    
    def test_with_dicts(self):
        """Prueba con diccionarios como elementos."""
        data = [
            {"a": 1, "b": 2},
            {"a": 1, "b": 2},
            {"x": 10, "y": 20},
            {"x": 10, "y": 20},
        ]
        result = find_duplicates_and_count(data)
        result_dict = {tuple(sorted(item[0].items())): item[1] for item in result}
        
        self.assertEqual(len(result), 2)
        # Verificar que ambos tipos de diccionarios fueron encontrados
        counts = {item[1] for item in result}
        self.assertEqual(counts, {2})
        print("✓ Test con diccionarios pasado")
    
    def test_with_mixed_types(self):
        """Prueba con tipos mixtos (hashables y no hashables)."""
        data = [
            42,
            42,
            "texto",
            "texto",
            [1, 2],
            [1, 2],
            3.14,
            3.14,
            3.14,
        ]
        result = find_duplicates_and_count(data)
        
        self.assertEqual(len(result), 4)
        # Crear diccionario con representación de elementos como claves
        result_dict = {}
        for elem, count in result:
            if isinstance(elem, list):
                result_dict[tuple(elem)] = count
            else:
                result_dict[elem] = count
        
        self.assertEqual(result_dict[42], 2)
        self.assertEqual(result_dict["texto"], 2)
        self.assertEqual(result_dict[(1, 2)], 2)
        self.assertEqual(result_dict[3.14], 3)
        print("✓ Test con tipos mixtos pasado")
    
    def test_with_nested_structures(self):
        """Prueba con estructuras anidadas complejas."""
        data = [
            {"list": [1, 2, 3], "value": 10},
            {"list": [1, 2, 3], "value": 10},
            {"list": [4, 5, 6], "value": 20},
        ]
        result = find_duplicates_and_count(data)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], 2)  # El único duplicado debe aparecer 2 veces
        print("✓ Test con estructuras anidadas pasado")
    
    def test_with_sets(self):
        """Prueba con sets como elementos."""
        data = [
            {1, 2, 3},
            {1, 2, 3},
            {4, 5},
            {4, 5},
            {4, 5},
        ]
        result = find_duplicates_and_count(data)
        
        self.assertEqual(len(result), 2)
        # Convertir a diccionario para verificación más fácil
        result_dict = {tuple(sorted(item[0])): item[1] for item in result}
        self.assertEqual(result_dict[(1, 2, 3)], 2)
        self.assertEqual(result_dict[(4, 5)], 3)
        print("✓ Test con sets pasado")
    
    def test_with_hashable_elements_still_works(self):
        """Verifica que elementos hashables normales aún funcionan."""
        data = [1, 1, 2, 2, 2, 3, "a", "a"]
        result = find_duplicates_and_count(data)
        
        self.assertEqual(len(result), 3)
        # Convertir a diccionario para verificación
        result_dict = {item[0]: item[1] for item in result}
        self.assertEqual(result_dict[1], 2)
        self.assertEqual(result_dict[2], 3)
        self.assertEqual(result_dict["a"], 2)
        print("✓ Test con elementos hashables pasado")
    
    def test_large_list_with_non_hashable(self):
        """Prueba de rendimiento con 10,000 elementos no hashables."""
        import time
        # Crear lista con 5,000 listas diferentes, cada una repetida 2 veces
        data = []
        for i in range(5000):
            data.extend([[i, i+1], [i, i+1]])
        
        start_time = time.time()
        result = find_duplicates_and_count(data)
        end_time = time.time()
        
        execution_time = end_time - start_time
        
        print(f"\n--- Rendimiento con 10,000 elementos no hashables ---")
        print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
        print(f"Elementos únicos duplicados: {len(result)}")
        
        self.assertEqual(len(result), 5000)
        # Verificar que todos tienen conteo de 2
        for elem, count in result:
            self.assertEqual(count, 2)
        print("✓ Test de rendimiento con listas pasado")


if __name__ == '__main__':
    unittest.main(verbosity=2)
