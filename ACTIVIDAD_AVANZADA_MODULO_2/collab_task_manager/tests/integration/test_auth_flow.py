from tests.conftest import BaseIntegrationTest
from app.services.auth_service import AuthService
from app.core.security import SECRET_KEY, ALGORITHM
import jwt

class TestAuthFlow(BaseIntegrationTest):
    def test_full_auth_cycle(self):
        # 1. Registro
        user = AuthService.register_user("test_user", "Password123!")
        
        # Guardas para Pylance y validación de test
        self.assertIsNotNone(user, "El registro falló y devolvió None")
        
        if user:  # Aquí Pylance ya sabe que user no es None
            self.assertEqual(user['username'], "test_user")
            self.assertIsInstance(user['id'], int)

            # 2. Autenticación (Login)
            token = AuthService.authenticate("test_user", "Password123!")
            self.assertIsNotNone(token, "El token no debería ser None tras un login válido")
            
            if token:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                self.assertEqual(payload['role'], 'user')
                # Verificamos que el ID coincida (usando str para evitar líos de tipos en JWT)
                self.assertEqual(str(payload['sub']), str(user['id']))
        
    def test_invalid_login(self):
        # Registramos un usuario pero probamos con pass incorrecta
        AuthService.register_user("user2", "pass123")
        token = AuthService.authenticate("user2", "wrong_pass")
        self.assertIsNone(token)