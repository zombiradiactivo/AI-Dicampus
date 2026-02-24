from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 1. Atributos comunes (Lo que comparten todas las versiones de "Usuario")
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# 2. Esquema para el REGISTRO (Entrada)
class UserCreate(UserBase):
    # Añadimos max_length=72 para evitar que bcrypt explote
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=72, 
        description="La contraseña debe tener entre 8 y 72 caracteres"
    )
# 3. Esquema para devolver datos al CLIENTE (Salida)
# ¡NUNCA incluyas el password aquí!
class User(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class Config:
        # Esto permite que Pydantic lea datos aunque sean objetos de SQLAlchemy (ORM)
        from_attributes = True

# 4. Esquema para el TOKEN de respuesta
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None