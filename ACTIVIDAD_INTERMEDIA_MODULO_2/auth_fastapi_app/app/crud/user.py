from sqlalchemy.orm import Session
from app.models import user as user_models
from app.schemas import user as user_schemas
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    """Busca un usuario en la base de datos por su correo electrónico."""
    return db.query(user_models.User).filter(user_models.User.email == email).first()

def create_user(db: Session, user: user_schemas.UserCreate):
    """
    Crea un nuevo usuario transformando la contraseña en un hash 
    antes de guardarla en la base de datos.
    """
    # 1. Hasheamos la contraseña que viene del Schema
    hashed_pw = get_password_hash(user.password)
    
    # 2. Creamos la instancia del Modelo (Base de Datos)
    db_user = user_models.User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_pw
    )
    
    # 3. Guardamos en la BD
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user