from app.services.audit_service import record_action
from app.database import repository

def get_system_audit_logs(current_user: dict):
    if current_user['role'] != 'admin':
        return {"error": "Forbidden", "status": 403}
    
    logs = repository.get_all_audit_logs()
    record_action(current_user['id'], "VIEW_AUDIT_LOGS", "System")
    return {"data": logs, "status": 200}