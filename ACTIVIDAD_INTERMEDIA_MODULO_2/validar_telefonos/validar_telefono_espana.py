import re

def validar_telefono_espana(telefono: str) -> bool:
    """
    Valida si un número de teléfono sigue el formato internacional español.
    
    El formato requerido es: '+34' seguido exactamente de 9 dígitos numéricos.
    
    Args:
        telefono (str): La cadena de texto con el número a validar.
        
    Returns:
        bool: True si el formato es válido, False en caso contrario.
    """
    # Explicación del patrón:
    # ^      : Inicio de la cadena
    # \+34   : El literal '+34' (escapamos el + porque es un caracter especial)
    # [6789] : El primer dígito suele empezar por 6, 7 (móviles) o 8, 9 (fijos)
    # \d{8}  : Exactamente 8 dígitos numéricos adicionales
    # $      : Fin de la cadena
    patron = r"^\+34[6789]\d{8}$"
    
    return bool(re.match(patron, telefono))

# --- Casos de Prueba ---
pruebas = [
    "+34600111222",  # Válido (Móvil)
    "+34912345678",  # Válido (Fijo)
    "600111222",     # Inválido (Falta el prefijo +34)
    "+34123456789",  # Inválido (Empieza por 1, no es un rango estándar)
    "+346001112223", # Inválido (Tiene 10 dígitos en lugar de 9)
    "34600111222",   # Inválido (Falta el símbolo +)
]

print("Resultados de la validación:")
for t in pruebas:
    resultado = "✅ Válido" if validar_telefono_espana(t) else "❌ Inválido"
    print(f"{t}: {resultado}")