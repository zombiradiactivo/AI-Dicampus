from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import cast # Importa cast para ayudar al linter
from app.crud import user as user_crud
from app.schemas import user as user_schemas
from app.core import security
from app.database import SessionLocal
from jose import JWTError, jwt
from app.models.user import User as UserModel

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
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = user_crud.get_user_by_email(db, email=form_data.username)
    
    # 1. Verificamos si el usuario existe primero
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    # 2. Usamos 'cast' para decirle al linter: "Confía en mí, esto es un str"
    # O simplemente extraemos el valor si el linter sigue protestando
    is_password_correct = security.verify_password(
        form_data.password, 
        cast(str, user.hashed_password) 
    )

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generar el Token
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
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