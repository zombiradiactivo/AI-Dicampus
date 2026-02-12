import unittest
import tkinter as tk
from calc_gui import realizar_operacion, entry_1, entry_2, label_resultado

class TestCalculadoraGUI(unittest.TestCase):

    def setUp(self):
        """Limpia las entradas antes de cada prueba."""
        entry_1.delete(0, tk.END)
        entry_2.delete(0, tk.END)
        label_resultado.config(text="Resultado: 0")

    def test_suma_gui(self):
        # 1. Simulamos que el usuario escribe 10 y 5
        entry_1.insert(0, "10")
        entry_2.insert(0, "5")
        
        # 2. Ejecutamos la función que llamaría el botón
        realizar_operacion("sumar")
        
        # 3. Verificamos si la etiqueta cambió al valor correcto
        self.assertEqual(label_resultado.cget("text"), "Resultado: 15.0")

    def test_resta_gui(self):
        entry_1.insert(0, "20")
        entry_2.insert(0, "8")
        realizar_operacion("restar")
        self.assertEqual(label_resultado.cget("text"), "Resultado: 12.0")

    def test_multiplicar_gui(self):
        entry_1.insert(0, "10")
        entry_2.insert(0, "5")
        realizar_operacion("multiplicar")
        self.assertEqual(label_resultado.cget("text"), "Resultado: 50.0")

    def test_division_por_cero_gui(self):
        entry_1.insert(0, "10")
        entry_2.insert(0, "0")
        
        # Ahora coinciden: el código lanza ZeroDivisionError y el test busca ZeroDivisionError
        with self.assertRaises(ZeroDivisionError):
            realizar_operacion("dividir")

    def test_division_numerador_cero(self):
        entry_1.insert(0, "0")
        entry_2.insert(0, "5")
        with self.assertRaises(ZeroDivisionError):
            realizar_operacion("dividir")

if __name__ == "__main__":
    unittest.main()