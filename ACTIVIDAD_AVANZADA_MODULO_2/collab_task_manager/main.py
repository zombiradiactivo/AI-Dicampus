from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
# Importamos el servicio y la seguridad para procesar el token
from app.core.security import SECRET_KEY, ALGORITHM
import jwt
from app.services.task_service import TaskService

from app.api.tasks import get_tasks_endpoint
from app.services.auth_service import AuthService
from app.core.security import create_access_token
from app.services.task_service import TaskService
import uvicorn

app = FastAPI(title="Collab Task Manager")

# Modelos para validación de entrada
class UserAuth(BaseModel):
    username: str
    password: str

# Montar estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# --- ENDPOINTS DE AUTENTICACIÓN ---

@app.post("/api/register")
async def register(user: UserAuth):
    # Primero verificamos si el usuario ya existe (usando el nombre, no authenticate)
    from app.database import repository
    if repository.get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")
    
    new_user = AuthService.register_user(user.username, user.password)
    
    # VALIDACIÓN: Verificamos que new_user no sea None antes de acceder a ['id']
    if new_user is None:
        raise HTTPException(
            status_code=500, 
            detail="Error crítico: No se pudo crear el usuario en la base de datos"
        )
    
    return {"message": "Usuario creado con éxito", "user_id": new_user['id']}


@app.post("/api/login")
async def login(user_data: UserAuth):
    # Obtenemos el usuario de la DB
    from app.database import repository
    user = repository.get_user_by_username(user_data.username)
    
    # VALIDACIÓN PARA PYLANCE: Comprobamos que user no sea None
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
        
    # Ahora validamos la contraseña usando tu AuthService
    token = AuthService.authenticate(user_data.username, user_data.password)
    
    if not token:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
        
    return {"access_token": token, "token_type": "bearer"}

# --- ENDPOINTS DE TAREAS ---

@app.get("/api/tasks")
async def tasks_route(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    # 1. Decodificar el token para saber quién es el usuario

    token = authorization.split(" ")[1]
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")

    # 2. Crear el servicio con el ID y el ROL del payload
    service = TaskService({
        "id": payload.get("sub"),
        "role": payload.get("role")
    })
    
    # 3. Obtener las tareas (el servicio ya sabe si filtrar o no)
    tasks = service.get_tasks()
    return {"data": tasks, "status": 200}


# Añade este modelo junto a UserAuth en main.py
class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int
    due_date: str

# Añade este endpoint después de tasks_route
@app.post("/api/tasks")
async def create_task_route(task: TaskCreate, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")
        
        # Usamos el TaskService que ya teníamos implementado
        service = TaskService({"id": user_id, "role": role})
        
        # Convertimos el modelo a dict y añadimos el user_id
        task_dict = task.model_dump()
        task_dict['user_id'] = user_id
        
        new_task = service.create_task(task_dict)
        return {"data": new_task, "status": 201}
        
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido o error: {str(e)}")

# Endpoint para borrar
@app.delete("/api/tasks/{task_id}")
async def delete_task_route(task_id: int, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401)
    
    # En un sistema real, aquí verificarías que la tarea pertenece al usuario
    from app.database import repository
    repository.delete_task(task_id) # Debes asegurarte que este método existe en repository.py
    return {"message": "Tarea borrada"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)