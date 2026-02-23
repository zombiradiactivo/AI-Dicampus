import random

def jugar_adivina_el_numero():
    print("--- ¡Bienvenido a Adivina el Número! ---")
    
    jugando = True
    puntuacion_total = 0

    while jugando:
        numero_secreto = random.randint(1, 100)
        intentos_restantes = 7
        ganado = False
        
        print(f"\nHe pensado un número entre 1 y 100. Tienes {intentos_restantes} intentos.")

        while intentos_restantes > 0:
            try:
                # 4. Entrada del usuario
                prediccion = int(input(f"\n[Intentos restantes: {intentos_restantes}] Introduce tu número: "))
            except ValueError:
                print("Por favor, introduce un número válido.")
                continue

            # 3. Pistas y lógica
            if prediccion < numero_secreto:
                print("Más ALTO ↑")
            elif prediccion > numero_secreto:
                print("Más BAJO ↓")
            else:
                ganado = True
                break
            
            intentos_restantes -= 1

        # Manejo de resultados y puntuación
        if ganado:
            puntos_ganados = intentos_restantes * 10 # 4. Registro de puntuación
            puntuacion_total += puntos_ganados
            print(f"¡Felicidades! Adivinaste el número {numero_secreto}.")
            print(f"Ganaste {puntos_ganados} puntos en esta ronda.")
        else:
            print(f"Se acabaron los intentos. El número era {numero_secreto}.")

        print(f"PUNTUACIÓN TOTAL: {puntuacion_total}")

        # 5. Preguntar si quiere jugar otra vez
        respuesta = input("\n¿Quieres jugar de nuevo? (s/n): ").lower()
        if respuesta != 's':
            jugando = False
            print(f"\nGracias por jugar. Tu puntuación final fue: {puntuacion_total}")

if __name__ == "__main__":
    jugar_adivina_el_numero()