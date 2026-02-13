class Calculadora:
    def sumar(self, a, b):
        return a + b

    def restar(self, a, b):
        return a - b

    def multiplicar(self, a, b):
        return a * b

    def dividir(self, a, b):
        if b == 0:
            raise ValueError("Error: No se puede dividir por cero.")
        if a == 0:
            raise ValueError("Error: No se puede dividir por cero.")
        return a / b

def menu():
    calc = Calculadora()
    
    while True:
        print("\n--- Calculadora Simple ---")
        print("1. Sumar")
        print("2. Restar")
        print("3. Multiplicar")
        print("4. Dividir")
        print("5. Salir")
        
        opcion = input("Elige una opción (1-5): ")

        if opcion == '5':
            print("¡Hasta luego!")
            break

        if opcion in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Introduce el primer número: "))
                num2 = float(input("Introduce el segundo número: "))

                if opcion == '1':
                    print(f"Resultado: {calc.sumar(num1, num2)}")
                elif opcion == '2':
                    print(f"Resultado: {calc.restar(num1, num2)}")
                elif opcion == '3':
                    print(f"Resultado: {calc.multiplicar(num1, num2)}")
                elif opcion == '4':
                    print(f"Resultado: {calc.dividir(num1, num2)}")
            
            except ValueError as e:
                print(f"Error: Entrada no válida. {e}")
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    menu()