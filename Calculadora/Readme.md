# Proyecto: Calculadora Python con GUI y Pruebas Unitarias

Este proyecto implementa una calculadora modular en Python que ofrece tanto una interfaz de línea de comandos (CLI) como una interfaz gráfica de usuario (GUI). Además, incluye una suite completa de pruebas unitarias para garantizar la fiabilidad del código.

## 📂 Estructura del Repositorio

| Archivo | Función |
| :--- | :--- |
| `calc.py` | Contiene la lógica central (clase `Calculadora`) y el menú de consola. |
| `calc_gui.py` | Implementación de la interfaz visual con la librería `tkinter`. |
| `Test.py` | Suite de pruebas unitarias para la lógica matemática básica. |
| `Test_for_gui.py` | Pruebas de integración para validar el comportamiento de la interfaz. |

---

## 🛠️ Componentes Principales

### 1. Lógica y Consola (`calc.py`)
La clase `Calculadora` encapsula las operaciones matemáticas:
* **Suma, Resta y Multiplicación:** Operaciones aritméticas estándar.
* **División con Validación:** El sistema lanza un `ValueError` si se intenta dividir por cero o si el dividendo es cero.
* **Interfaz de Usuario:** Incluye un bucle `while` para interactuar mediante el terminal.

### 2. Interfaz Gráfica (`calc_gui.py`)
Desarrollada con **Tkinter**, permite una interacción más intuitiva:
* **Entradas:** Campos `entry_1` y `entry_2` para capturar datos del usuario.
* **Botones:** Acciones vinculadas a funciones lambda para ejecutar las operaciones.
* **Manejo de Errores:** Muestra cuadros de diálogo (messagebox) si la entrada no es un número válido.

### 3. Suite de Pruebas (`unittest`)
Se han implementado dos niveles de testeo:
* **Pruebas de Lógica (`Test.py`):** Verifica resultados exactos y la correcta activación de excepciones.
* **Pruebas de GUI (`Test_for_gui.py`):** Simula la interacción del usuario insertando valores en los widgets y verificando la etiqueta de resultado.

---

## 🚀 Instalación y Uso

### Requisitos previos
* Python 3.x
* Tkinter (incluido por defecto en la mayoría de las instalaciones de Python)

### Ejecución de la Aplicación
Para iniciar la calculadora con interfaz gráfica:

```bash
python calc_gui.py
```

Para usar la versión de terminal:
```Bash
python calc.py
```
Ejecución de Pruebas

Es recomendable ejecutar las pruebas para asegurar que el entorno es estable:
```Bash
# Probar la lógica central
python -m unittest Test.py

# Probar la interfaz gráfica
python -m unittest Test_for_gui.py
```