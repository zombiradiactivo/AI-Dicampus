import unittest
from calc import Calculadora

class TestCalculadora(unittest.TestCase):
    
    def setUp(self):
        """Se ejecuta antes de cada test para crear una instancia fresca."""
        self.calc = Calculadora()

    def test_suma(self):
        self.assertEqual(self.calc.sumar(10, 5), 15)
        self.assertEqual(self.calc.sumar(-1, 1), 0)

    def test_resta(self):
        self.assertEqual(self.calc.restar(10, 5), 5)
        self.assertEqual(self.calc.restar(5, 10), -5)

    def test_multiplicacion(self):
        self.assertEqual(self.calc.multiplicar(3, 7), 21)
        self.assertEqual(self.calc.multiplicar(5, 0), 0)

    def test_division(self):
        self.assertEqual(self.calc.dividir(10, 2), 5)
        # Probamos que lance error al dividir por cero
        with self.assertRaises(ValueError):
            self.calc.dividir(10, 0)
            self.calc.dividir(0, 10)

if __name__ == "__main__":
    unittest.main()