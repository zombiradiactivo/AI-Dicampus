import sqlite3
import unittest
from app.database import repository

def setup_test_db():
    conn = sqlite3.connect(repository.DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks")
    cursor.execute("DELETE FROM users")
    cursor.execute("DELETE FROM audit_logs") # Limpiar logs
    cursor.execute("DELETE FROM sqlite_sequence") # Resetear todos los contadores
    conn.commit()
    conn.close()

class BaseIntegrationTest(unittest.TestCase):
    def setUp(self):
        setup_test_db()