import hashlib
import os
import jwt # Standard para JWT
from datetime import datetime, timedelta, timezone

SECRET_KEY = os.getenv("JWT_SECRET", "super-secret-key")
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    """Crea un hash seguro usando PBKDF2."""
    salt = os.urandom(16)
    db_password = hashlib.pbkdf2_hmac(
        'sha256', password.encode(), salt, 100000
    )
    return salt.hex() + ":" + db_password.hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash guardado."""
    salt_hex, hash_hex = stored_password.split(":")
    salt = bytes.fromhex(salt_hex)
    expected_hash = hashlib.pbkdf2_hmac(
        'sha256', provided_password.encode(), salt, 100000
    ).hex()
    return expected_hash == hash_hex

def create_access_token(data: dict):
    to_encode = data.copy()
    # Expira en 1 hora para los tests
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None