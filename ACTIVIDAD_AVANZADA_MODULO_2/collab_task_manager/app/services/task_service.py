from app.database import repository
from app.services.audit_service import record_action

class TaskService:
    def __init__(self, user_context: dict):
        """
        user_context debe contener 'id' y 'role' 
        extraídos del token JWT.
        """
        self.user_id = user_context.get("id")
        self.role = user_context.get("role")
        
    def get_tasks(self):
        # Si es admin, recupera todo. Si no, solo lo suyo.
        if self.role == "admin":
            return repository.fetch_all_tasks()
        return repository.fetch_tasks_by_user(self.user_id)
    
    def create_task(self, task_data: dict):
        # Aquí puedes añadir validaciones de negocio adicionales
        return repository.save_task(task_data)