import tkinter as tk
from tkinter import messagebox

def realizar_operacion(operacion):
    try:
        # Obtenemos los números de las entradas
        num1 = float(entry_1.get())
        num2 = float(entry_2.get())
        
        if operacion == "sumar":
            resultado = num1 + num2
        elif operacion == "restar":
            resultado = num1 - num2
        elif operacion == "multiplicar":
            resultado = num1 * num2
        elif operacion == "dividir":
            if num1 == 0:
                messagebox.showerror("Error", "No se puede dividir por cero.")
                raise ZeroDivisionError("Error: No se puede dividir por cero.")
            if num2 == 0:
                messagebox.showerror("Error", "No se puede dividir por cero.")
                raise ZeroDivisionError("Error: No se puede dividir por cero.")
            resultado = num1 / num2
        
        # Actualizamos la etiqueta del resultado
        label_resultado.config(text=f"Resultado: {resultado}", fg="black")
    except ValueError:
            # Error si el usuario no ingresa números válidos
            messagebox.showerror("Error", "Por favor, ingresa solo números.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Calculadora Básica")
ventana.geometry("300x250")
ventana.resizable(False, False)

# Elementos de la interfaz (Widgets)
tk.Label(ventana, text="Número 1:", font=("Arial", 10)).pack(pady=5)
entry_1 = tk.Entry(ventana, justify="center")
entry_1.pack()

tk.Label(ventana, text="Número 2:", font=("Arial", 10)).pack(pady=5)
entry_2 = tk.Entry(ventana, justify="center")
entry_2.pack()

# Contenedor para los botones
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=20)

btn_sumar = tk.Button(frame_botones, text="Sumar (+)", width=10, 
                      command=lambda: realizar_operacion("sumar"), bg="#b5e3f8")
btn_sumar.grid(row=0, column=0, padx=5)

btn_restar = tk.Button(frame_botones, text="Restar (-)", width=10, 
                       command=lambda: realizar_operacion("restar"), bg="#adf4f7")
btn_restar.grid(row=0, column=1, padx=5)

btn_restar = tk.Button(frame_botones, text="Multiplicar (*)", width=10, 
                       command=lambda: realizar_operacion("multiplicar"), bg="#82d5fc")
btn_restar.grid(row=1, column=0, padx=5, pady=5)

btn_restar = tk.Button(frame_botones, text="Dividir (/)", width=10, 
                       command=lambda: realizar_operacion("dividir"), bg="#a7f0fa")
btn_restar.grid(row=1, column=1, padx=5, pady=5)

# Etiqueta para mostrar el resultado
label_resultado = tk.Label(ventana, text="Resultado: 0", font=("Arial", 12, "bold"))
label_resultado.pack(pady=10)

# Iniciar la aplicación
if __name__ == "__main__":
    ventana.mainloop()