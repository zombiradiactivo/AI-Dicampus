from datetime import datetime, timedelta, timezone
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.audit import LoginLog
from app.schemas.audit import LoginLogCreate

def create_login_log(db: Session, log_data: LoginLogCreate):
    """Registra un nuevo intento de inicio de sesión."""
    db_log = LoginLog(**log_data.model_dump())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_user_login_history(db: Session, email: str, limit: int = 10):
    """Consulta los últimos N intentos de login de un email específico."""
    return db.query(LoginLog).filter(LoginLog.email == email)\
             .order_by(desc(LoginLog.timestamp)).limit(limit).all()

def count_recent_failures(db: Session, email: str, minutes: int = 1) -> int:
    # 1. Usar UTC para evitar desfases con la base de datos
    # Si usas Python 3.12+ usa datetime.now(timezone.utc)
    since = datetime.now(timezone.utc) - timedelta(minutes=minutes)
    
    # 2. Normalizar el email (minúsculas y sin espacios) por si acaso
    clean_email = email.strip().lower()

    # 3. Consulta con filtros corregidos
    logs = db.query(LoginLog).filter(
        func.lower(LoginLog.email) == clean_email,
        LoginLog.timestamp >= since
    ).order_by(desc(LoginLog.timestamp)).all()
    
    print(f"Buscando fallos para {clean_email} desde {since}")
    print(f"Logs encontrados con filtro: {len(logs)}")

    consecutive_failures = 0
    for log in logs:
        if bool(log.success):
            break
        consecutive_failures += 1
        
    return consecutive_failures