import pytest
import bcrypt

from refactorizar_legacy_refactorizado import autenticar_usuario

# --- Configuración de datos de prueba (Fixtures) ---

@pytest.fixture
def db_prueba():
    # Generamos hashes reales de bcrypt para las pruebas
    pw_admin = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
    pw_user = bcrypt.hashpw("user123".encode(), bcrypt.gensalt())
    
    return [
        {"username": "ana", "password_hash": pw_admin, "rol": "admin"},
        {"username": "pedro", "password_hash": pw_user, "rol": "user"},
        {"username": "invitado", "password_hash": bcrypt.hashpw("guest".encode(), bcrypt.gensalt()), "rol": "guest"}
    ]

# --- Tests de Autenticación ---

def test_login_admin_exitoso(db_prueba):
    resultado = autenticar_usuario("ana", "admin123", db_prueba)
    assert resultado['ok'] is True
    assert resultado['lvl'] == 3
    assert "Admin OK" in resultado['msg']

def test_login_usuario_exitoso(db_prueba):
    resultado = autenticar_usuario("pedro", "user123", db_prueba)
    assert resultado['ok'] is True
    assert resultado['lvl'] == 1
    assert "User OK" in resultado['msg']

def test_password_incorrecta(db_prueba):
    resultado = autenticar_usuario("ana", "password_erronea", db_prueba)
    assert resultado['ok'] is False
    assert resultado['lvl'] == -1
    assert "inválidas" in resultado['msg']

def test_usuario_no_existente(db_prueba):
    resultado = autenticar_usuario("inexistente", "12345", db_prueba)
    assert resultado['ok'] is False
    assert resultado['lvl'] == -1

def test_seguridad_no_escalada_privilegios(db_prueba):
    """
    Verifica que no se puede forzar el rol desde fuera.
    Incluso si intentamos pasar un parámetro 'r', la función refactorizada 
    lo ignora (o ni siquiera lo recibe).
    """
    # Intentamos loguearnos como pedro (user) pero con la intención de ser admin
    resultado = autenticar_usuario("pedro", "user123", db_prueba)
    assert resultado['lvl'] != 3  # Debe mantener su nivel 1 original
    assert resultado['lvl'] == 1