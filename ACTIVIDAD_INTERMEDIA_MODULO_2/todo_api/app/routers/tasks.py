from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
import app.models as models, app.database as database, app.schemas as schemas 
from app.schemas import TaskCreate, Task, TaskUpdate
 
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

# 1. GET - Leer tareas de la BD
@router.get("/", response_model=List[schemas.Task])
def read_tasks(db: Session = Depends(database.get_db)):
    return db.query(models.Task).all()

# 2. POST - Guardar en BD
@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    new_task = models.Task(**task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task) # Recargamos para obtener el ID generado
    return new_task

# 3. PUT - Actualizar en BD
@router.patch("/{task_id}", response_model=schemas.Task)
def patch_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    task_query = db.query(models.Task).filter(models.Task.id == task_id)
    task_db = task_query.first()
    
    if not task_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    # exclude_unset=True es la clave: solo toma los campos que el usuario envió explícitamente
    update_data = task_update.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(task_db, key, value)
    
    db.commit()
    db.refresh(task_db)
    return task_db
    
# 4. DELETE - Borrar de BD
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    task_db = db.query(models.Task).filter(models.Task.id == task_id).first()
    
    if not task_db:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    
    db.delete(task_db)
    db.commit()
    return {"message": "Tarea eliminada correctamente"}