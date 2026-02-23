from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel, Field
from typing import Optional

class TaskBase(BaseModel):
    # El título no puede ser vacío y limitamos la longitud
    title: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    completed: bool = False

class TaskCreate(TaskBase):
    pass

# Nuevo esquema para PATCH (ver punto 2)
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    class Config:
        from_attributes = True