import jwt
from app.core.security import SECRET_KEY, ALGORITHM
from app.core.middleware import check_rate_limit, audit_log_interceptor
from app.services.task_service import TaskService
from app.core.security import decode_access_token

def get_tasks_endpoint(auth_header: str):
    try:
        if not auth_header or "Bearer " not in auth_header:
                return {"error": "Missing token", "status": 401}

        token = auth_header.split(" ")[1]
        payload = decode_access_token(token) # <--- Usa la función centralizada

        if not payload:
            return {"error": "Invalid token", "status": 401}

        # El 'sub' en el JWT suele ser el ID del usuario
        user_context = {
            "id": payload.get("sub"),
            "role": payload.get("role")
        }
        
        service = TaskService(user_context)
        tasks = service.get_tasks()
            
        return {"data": tasks, "status": 200}        
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired", "status": 401}
    except jwt.PyJWTError:
        return {"error": "Invalid token", "status": 401}
    except Exception as e:
        return {"error": str(e), "status": 500}
    
    