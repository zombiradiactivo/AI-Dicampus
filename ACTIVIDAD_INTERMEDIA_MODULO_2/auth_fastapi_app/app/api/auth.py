from fastapi import Request
from datetime import timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from typing import cast # Importa cast para ayudar al linter

from app.core import security
from app.database import SessionLocal
from app.crud import user as user_crud
from app.crud import audit as audit_crud
from app.models import user as user_models
from app.schemas import user as user_schemas
from app.models.user import User as UserModel
from app.schemas import audit as audit_schemas


router = APIRouter(prefix="/auth", tags=["auth"])



# Dependencia para obtener la sesión de BD en cada petición
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=user_schemas.User)
def register_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    """Crea un nuevo usuario si el email no está registrado."""
    db_user = user_crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El email ya está registrado"
        )
    return user_crud.create_user(db=db, user=user)

@router.post("/login", response_model=user_schemas.Token)
def login_for_access_token(
    request: Request, # <--- Inyectamos el request para la IP
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)):

    # 1. Verificar si hay demasiados fallos previos (Seguridad)
    recent_failures = audit_crud.count_recent_failures(db, email=form_data.username)
    if recent_failures >= 5:
        raise HTTPException(
            status_code=429, 
            detail="Cuenta bloqueada temporalmente por demasiados intentos fallidos."
        )

    user = user_crud.get_user_by_email(db, email=form_data.username)
    ip = request.client.host if request.client else "unknown"
    
    success = False
    user_id_val: int | None = None # Usamos un nombre distinto para evitar confusiones   

    # 1. Verificamos usuario y contraseña
    if user and security.verify_password(form_data.password, cast(str, user.hashed_password)):
        success = True
        user_id_val = cast(int, user.id) # 'cast' le dice al linter que esto es un int

    # 3. REGISTRAR EN AUDITORÍA
    audit_crud.create_login_log(db, audit_schemas.LoginLogCreate(
        email=form_data.username,
        ip_address=ip,
        success=success,
        user_id=user_id_val
    ))

    if not success or not user: # Añadimos 'not user' para que el linter sepa que no es None abajo
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
# 3. Generar Token
    # Ahora el linter sabe que 'user' no es None gracias al if anterior
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=cast(str, user.email), 
        expires_delta=access_token_expires    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# 1. Función para obtener el usuario actual desde el Token
def get_current_user(db: Session = Depends(get_db), token: str = Depends(security.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        
        # 1. Obtenemos el valor (que técnicamente puede ser Any | None)
        sub_value = payload.get("sub")
        # 2. Verificamos que no sea None y que sea un string
        if sub_value is None or not isinstance(sub_value, str):
            raise credentials_exception
        # 3. Ahora el linter sabe que 'email' es 'str' 100% seguro
        email: str = sub_value 
        
    except JWTError:
        raise credentials_exception
        
    user = user_crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# 2. Ruta protegida: Solo accesible con Token válido
@router.get("/me", response_model=user_schemas.User)
def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user

@router.get("/logs/{email}", response_model=list[audit_schemas.LoginLog])
def read_login_history(
    email: str, 
    db: Session = Depends(get_db),
    current_user: user_models.User = Depends(get_current_user) # Protegido
):
    """Devuelve el historial de accesos de un email."""
    # Podrías añadir lógica aquí para que un usuario solo vea sus propios logs
    return audit_crud.get_user_login_history(db, email=email)