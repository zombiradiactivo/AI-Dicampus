from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional # Añadido

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    DONE = "done"

@dataclass
class Task:
    id: int
    title: str
    description: str
    priority: int
    due_date: datetime
    status: str = "todo"
    user_id: Optional[int] = None # Corregido: Ahora acepta None
    created_at: datetime = field(default_factory=datetime.now)