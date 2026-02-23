from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- Importar esto
from app.routers import tasks
from app.database import engine
import app.models as models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000", # Ejemplo: Frontend de React
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # O usa ["*"] para permitir a TODO el mundo (menos seguro)
    allow_credentials=True,
    allow_methods=["*"],   # Permitir GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "API de Tareas con Base de Datos SQLite"}