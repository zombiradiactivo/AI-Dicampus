from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.database import engine, Base
from app.core.config import settings

print(f"La base de datos configurada es: {settings.DATABASE_URL}")
# Crear las tablas en la base de datos (solo para desarrollo)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Autenticación")

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "API de Autenticación funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)