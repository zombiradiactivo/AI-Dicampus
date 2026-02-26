# app/api/auth.py
import jwt
from app.core.security import SECRET_KEY, ALGORITHM, create_access_token
from app.core.config import settings

def refresh_token_endpoint(refresh_token: str):
    try:
        # Pylance puede quejarse de jwt.decode si no tienes tipos instalados, 
        # pero funcionalmente es correcto con PyJWT
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if payload.get("type") != "refresh":
            return {"error": "Invalid token type", "status": 401}
            
        new_token = create_access_token(
            data={"sub": payload["sub"], "role": payload["role"]}
        )
        return {"access_token": new_token, "status": 200}
    except jwt.PyJWTError: # Mejor usar la excepción base de PyJWT
        return {"error": "Invalid token", "status": 401}