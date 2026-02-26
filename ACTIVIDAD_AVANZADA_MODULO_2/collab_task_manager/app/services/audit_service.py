from datetime import datetime, timezone

def record_action(user_id: int, action: str, details: str):
    """
    Formatea y persiste el log de auditoría.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "user_id": user_id,
        "action": action,
        "details": details
    }
    
    # En una app real, esto iría a una tabla 'audit_logs' o un servicio de logging externo
    print(f"AUDIT_LOG: {log_entry}")
    
    with open("logs/audit.log", "a") as f:
        f.write(f"{timestamp} | USER:{user_id} | ACT:{action} | {details}\n")