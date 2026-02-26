from tests.conftest import BaseIntegrationTest
from app.database import repository
from app.api.tasks import get_tasks_endpoint
from app.core.security import create_access_token

class TestTaskAccess(BaseIntegrationTest):
    def test_user_isolation(self):
        # Usamos IDs enteros que SQLite entiende bien
        repository.save_task({"title": "T1", "user_id": 1, "status": "todo", "priority": 1})
        repository.save_task({"title": "T2", "user_id": 2, "status": "todo", "priority": 1})

        token_u1 = create_access_token({"sub": 1, "role": "user"})
        response = get_tasks_endpoint(f"Bearer {token_u1}")

        # Si falla, el mensaje nos dirá por qué (401, 404, etc)
        self.assertEqual(response.get("status"), 200, f"La API falló con: {response}")
        self.assertIn('data', response)
        self.assertEqual(len(response['data']), 1)

    def test_admin_visibility(self):
        repository.save_task({"title": "T1", "user_id": 1, "status": "todo"})
        token_admin = create_access_token({"sub": 99, "role": "admin"})
        response = get_tasks_endpoint(f"Bearer {token_admin}")

        self.assertEqual(response.get("status"), 200, f"Error Admin: {response}")
        self.assertEqual(len(response['data']), 2)