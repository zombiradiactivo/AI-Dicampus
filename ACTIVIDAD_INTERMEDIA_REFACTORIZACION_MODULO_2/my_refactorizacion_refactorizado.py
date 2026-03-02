from dataclasses import dataclass
from typing import List

# Constantes para eliminar "Magic Numbers"
LIMITE_SALARIO_ALTO = 3000
INCREMENTO_ALTO = 1.1
INCREMENTO_BAJO = 1.05
BONUS_SENIOR = 0.20
BONUS_JUNIOR = 0.05

@dataclass
class Empleado:
    nombre: str
    salario_base: float
    rango: str

class CalculadoraFinanciera:
    """Clase con Cohesión Alta: Solo se encarga de cálculos."""
    
    @staticmethod
    def calcular_salario_final(base: float) -> float:
        factor = INCREMENTO_ALTO if base > LIMITE_SALARIO_ALTO else INCREMENTO_BAJO
        return base * factor

    @staticmethod
    def calcular_bono(salario: float, rango: str) -> float:
        porcentaje = BONUS_SENIOR if rango == "Senior" else BONUS_JUNIOR
        return salario * porcentaje

class ReporteEmpleado:
    """Clase encargada de la salida (Single Responsibility Principle)."""
    
    def generar(self, empleado: Empleado):
        calc = CalculadoraFinanciera()
        s_final = calc.calcular_salario_final(empleado.salario_base)
        bono = calc.calcular_bono(s_final, empleado.rango)
        
        print(f"--- Reporte: {empleado.nombre} ---")
        print(f"Salario final: {s_final:.2f}")
        print(f"Bonus: {bono:.2f}")
        print(f"Total: {(s_final + bono):.2f}")
        print("-" * 20)

# Ejecución limpia
empleados = [
    Empleado("Alex", 4000, "Senior"),
    Empleado("Santi", 2500, "Junior")
]

reportero = ReporteEmpleado()
for emp in empleados:
    reportero.generar(emp)