from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="API de Autenticación")

# --- Modelos de datos ---
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: Optional[str] = None

# --- Base de datos simulada ---
# En un entorno real, las contraseñas DEBEN estar hasheadas (ej. con passlib)
USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "password123",  # ¡Nunca guardes texto plano en producción!
        "email": "admin@example.com"
    }
}

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> Token:
    """
    Endpoint para autenticar usuarios y obtener un token de acceso.

    Args:
        form_data (OAuth2PasswordRequestForm): Objeto que contiene 'username' y 'password'.
            Este componente es inyectado automáticamente por FastAPI.

    Returns:
        Token: Un objeto Pydantic con el access_token y el tipo de token.

    Raises:
        HTTPException: Si las credenciales son incorrectas (401 Unauthorized).
    """
    user_dict = USERS_DB.get(form_data.username)
    
    # Validación simple (Simulada)
    if not user_dict or form_data.password != user_dict["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Aquí normalmente generarías un JWT (JSON Web Token)
    return Token(access_token=f"fake-jwt-token-for-{form_data.username}", token_type="bearer")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)