from app.core.security import hash_password, verify_password, create_access_token
from app.database import repository

class AuthService:
    @staticmethod
    def register_user(username, password):
        hashed = hash_password(password)
        user_data = {
        "username": username,
        "password_hash": hashed,
        "role": "user"}
        return repository.save_user(user_data) # Esto devuelve el dict con el ID de SQLite
    
    @staticmethod
    def authenticate(username, password):
        user = repository.get_user_by_username(username)
        if user and verify_password(user['password_hash'], password):
            token = create_access_token({"sub": str(user['id']), "role": user['role']})
            return token
        return None