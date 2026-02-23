# Validador de Teléfonos Españoles 🇪🇸

Este proyecto proporciona una solución sencilla y robusta para validar números de teléfono de España con formato internacional (`+34` seguido de 9 dígitos) tanto en **Python** como en **JavaScript**.

## 📋 Características
- Valida el prefijo internacional `+34`.
- Verifica que el número tenga exactamente 9 dígitos tras el prefijo.
- Restringe el primer dígito a rangos válidos en España (6, 7, 8 y 9).
- Incluye tipado (Type Hints / JSDoc) y documentación interna.

---

## 🐍 Versión Python

### Requisitos
- Python 3.6 o superior.

### Código (`validador.py`)
```python
import re

def validar_telefono_espana(telefono: str) -> bool:
    """Valida formato +34XXXXXXXXX."""
    patron = r"^\+34[6789]\d{8}$"
    return bool(re.match(patron, telefono))

# Ejemplo de uso
print(validar_telefono_espana("+34600111222")) # True
```

## Ejecución

Abre tu terminal y ejecuta:
```Bash
python validador.py
```

## 🟨 Versión JavaScript
### Requisitos

    Un navegador moderno (Chrome, Firefox, etc.) o Node.js instalado.

### Código (`validador.js`)
```JavaScript

/**
 * @param {string} telefono
 * @returns {boolean}
 */
function validarTelefonoEspana(telefono) {
    const patron = /^\+34[6789]\d{8}$/;
    return patron.test(telefono);
}

// Ejemplo de uso
console.log(validarTelefonoEspana("+34600111222")); // true
```
#### Ejecución
Con Node.js:
```Bash
node validador.js
```
#### En Navegador:
Copia el código y pégalo directamente en la consola de desarrollador (F12).
## ✅ Casos de Prueba Incluidos

| Entrada | Resultado | Motivo |
| :--- | :--- | :--- |
| +34600111222 | Válido | Formato móvil correcto. |
| +34912345678 | Válido | Formato fijo correcto. |
| 600111222 | Inválido | Falta el prefijo internacional. |
| +34511222333 | Inválido | Los números en España no empiezan por 5. |
| +346001112222 | Inválido | Longitud excesiva. |

## 🛠️ Tecnologías utilizadas

    Python: Utilizando el módulo nativo re.

    JavaScript: Utilizando expresiones regulares literales (/regex/).