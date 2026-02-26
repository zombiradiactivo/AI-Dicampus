import unittest
from datetime import datetime
# Asumiendo que el código anterior está en un archivo llamado spending_tracker.py
from Transacciones import Transaction, analyze_spending 

class TestAnalyzeSpending(unittest.TestCase):

    def setUp(self):
        """Configuración de datos de prueba."""
        self.transactions = [
            Transaction("1", 100.0, "EUR", datetime(2023, 5, 10), "Comida"),
            Transaction("2", 50.0, "USD", datetime(2023, 5, 15), "Transporte"),
            Transaction("3", 200.0, "EUR", datetime(2023, 6, 20), "Alquiler")
        ]

    def test_agrupacion_correcta(self):
        """Test 1: Verifica que agrupa correctamente por categoría en un mes específico."""
        # En mayo de 2023 hay 'Comida' (100) y 'Transporte' (50 USD -> ~46 EUR)
        resultado = analyze_spending(self.transactions, 5, 2023, base_currency='EUR')
        self.assertIn("Comida", resultado)
        self.assertIn("Transporte", resultado)
        self.assertEqual(len(resultado), 2)

    def test_conversion_moneda(self):
        """Test 2: Verifica que la conversión de USD a EUR se realiza (50 USD * 0.92 = 46 EUR)."""
        resultado = analyze_spending(self.transactions, 5, 2023, base_currency='EUR')
        # 50 USD * 0.92 = 46.0
        self.assertAlmostEqual(resultado["Transporte"], 46.0)

    def test_lista_vacia_lanza_error(self):
        """Test 3: Verifica que se lanza ValueError si la lista está vacía (Estrategia de Robustez)."""
        with self.assertRaises(ValueError) as cm:
            analyze_spending([], 5, 2023)
        self.assertEqual(str(cm.exception), 'Lista de transacciones vacía')

    def test_mes_sin_datos(self):
        """Test 4: Verifica el manejo de meses donde no hay transacciones."""
        # Buscamos en enero de 2023 (no hay datos)
        resultado = analyze_spending(self.transactions, 1, 2023)
        self.assertEqual(resultado, {})
        self.assertIsInstance(resultado, dict)

if __name__ == "__main__":
    unittest.main()