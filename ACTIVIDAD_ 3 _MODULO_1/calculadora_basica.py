# Archivo: calculadora_basica.py
# ESTO ES LO QUE TU LES MUESTRAS COMPLETO

import math

def suma(a, b):
    """Suma dos numeros"""

    return a + b

def resta(a, b):
    """Resta dos números"""

    return a - b

# PUNTO DE PARTIDA PARA LOS ALUMNOS:

# A partir de aquí, ellos usarán prompts para continuar

def multiplicacion(a, b):
    """Multiplica dos números"""
    return a * b

def division(a, b):
    """Divide dos números, manejando el error de división por cero"""
    if b == 0:
        raise ValueError("No se puede dividir entre cero.")
    return a / b

# --- NUEVAS FUNCIONES ---

def potencia(base, exponente):
    """Calcula la potencia de una base elevada a un exponente"""
    return base ** exponente

def raiz_cuadrada(numero):
    """Calcula la raíz cuadrada, manejando números negativos"""
    if numero < 0:
        raise ValueError("No se puede calcular la raíz cuadrada de un número negativo.")
    return math.sqrt(numero)

def calcular_porcentaje(porcentaje, total):
    """Calcula el porcentaje de un total dado"""
    return (porcentaje / 100) * total

# --- MENÚ INTERACTIVO ---

def mostrar_menu():
    print("\n--- Calculadora Pro ---")
    print("1. Sumar")
    print("2. Restar")
    print("3. Multiplicar")
    print("4. Dividir")
    print("5. Potencia")
    print("6. Raíz Cuadrada")
    print("7. Calcular Porcentaje")
    print("8. Salir")

def ejecutar_calculadora():
    while True:
        mostrar_menu()
        try:
            opcion = input("\nSelecciona una opción (1-8): ")
            
            if opcion == '8':
                print("¡Hasta luego!")
                break

            if opcion in ['1', '2', '3', '4', '5', '7']:
                n1 = float(input("Introduce el primer número: "))
                n2 = float(input("Introduce el segundo número: "))

                if opcion == '1': print(f"Resultado: {suma(n1, n2)}")
                elif opcion == '2': print(f"Resultado: {resta(n1, n2)}")
                elif opcion == '3': print(f"Resultado: {multiplicacion(n1, n2)}")
                elif opcion == '4': print(f"Resultado: {division(n1, n2)}")
                elif opcion == '5': print(f"Resultado: {potencia(n1, n2)}")
                elif opcion == '7': print(f"Resultado: {calcular_porcentaje(n1, n2)}")

            elif opcion == '6':
                n = float(input("Introduce el número: "))
                print(f"Resultado: {raiz_cuadrada(n)}")
            
            else:
                print("Opción no válida. Intenta de nuevo.")

        except ValueError as e:
            print(f"Error: {e}. Asegúrate de introducir números válidos.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    ejecutar_calculadora()