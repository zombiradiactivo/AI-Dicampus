import sqlite3
from app.core.config import settings

class DatabaseManager:
    _instance = None
    connection = None # Definir explícitamente a nivel de clase
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Aquí se inicializaría el pool de conexiones
            cls._instance.connection = None 
        return cls._instance

    def get_connection(self):
        # Lógica para retornar una conexión activa
        print(f"Connecting to {settings.DATABASE_URL}...")
        return self.connection

db_manager = DatabaseManager()