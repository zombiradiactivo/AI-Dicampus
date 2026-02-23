def validar_email(email):
    # 1. Verificar que no tenga espacios
    if " " in email:
        return False
    
    # 2. Verificar que tenga exactamente un '@'
    if email.count("@") != 1:
        return False
     
    # Dividimos el email en dos partes: usuario y dominio
    usuario, dominio = email.split("@")
    
    # 3. Verificar que haya un punto después del @ (en el dominio)
    # También validamos que el punto no sea el primer ni el último carácter
    if "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        return False
    
    # 4. Verificación adicional: que el usuario no esté vacío
    if len(usuario) == 0:
        return False

    return True

# --- Ejemplos de uso ---
emails_prueba = [
    "contacto@empresa.com",   # Válido
    "usuario@gmail",          # Inválido (sin punto tras @)
    "hola @mundo.com",        # Inválido (tiene espacio)
    "sin_arroba.com",         # Inválido (sin @)
    "doble@@punto.com",       # Inválido (doble @)
    "@sinusuario.com"         # Inválido (sin nombre de usuario)
]

print("Resultados de la validación:")
for e in emails_prueba:
    resultado = validar_email(e)
    print(f"{e.ljust(20)} -> {'✅ Válido' if resultado else '❌ Inválido'}")