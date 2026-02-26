from tests.conftest import BaseIntegrationTest
from app.api.tasks import get_tasks_endpoint
from app.core.security import create_access_token
from app.core.middleware import request_history

class TestRateLimiting(BaseIntegrationTest):
    def test_rate_limit_enforcement(self):
        # Crear un token válido
        token = create_access_token({"sub": 100, "role": "user"})
        auth_header = f"Bearer {token}"
        
        # Limpiar historial de intentos
        request_history.clear()

        # Realizar 100 peticiones (Límite máximo)
        for _ in range(100):
            response = get_tasks_endpoint(auth_header)
            # Verificamos que no sea el error de rate limit todavía
            self.assertNotEqual(response.get("status"), 429)

        # La petición 101 debe fallar con 429
        fail_response = get_tasks_endpoint(auth_header)
        self.assertEqual(fail_response.get("status"), 429)
        self.assertEqual(fail_response.get("error"), "Too many requests")