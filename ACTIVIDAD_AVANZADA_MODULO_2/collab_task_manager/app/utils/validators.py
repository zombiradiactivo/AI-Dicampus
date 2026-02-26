import re

def validate_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def validate_password_strength(password: str) -> bool:
    # Mínimo 8 caracteres, una mayúscula y un número
    return len(password) >= 8 and any(c.isdigit() for c in password)