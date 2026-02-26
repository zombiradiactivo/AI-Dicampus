import time
from datetime import datetime, timezone # Añadido
from collections import defaultdict

# Estructura simple en memoria para Rate Limiting
# user_id -> [timestamps de peticiones]
request_history = defaultdict(list)

def check_rate_limit(user_id: str) -> bool:
    """Retorna True si el usuario puede proceder, False si excedió el límite."""
    now = time.time()
    # Limpiar timestamps antiguos (más de 60 segundos)
    request_history[user_id] = [t for t in request_history[user_id] if now - t < 60]
    
    if len(request_history[user_id]) >= 100:
        return False
    
    request_history[user_id].append(now)
    return True

def audit_log_interceptor(user_id: str, action: str, resource: str):
    """Registra cada acción en el sistema."""
    timestamp = datetime.now(timezone.utc).isoformat()
    log_entry = f"[{timestamp}] User: {user_id} | Action: {action} | Resource: {resource}\n"
    
    with open("logs/audit.log", "a") as f:
        f.write(log_entry)