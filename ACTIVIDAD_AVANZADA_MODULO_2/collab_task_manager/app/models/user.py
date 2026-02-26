# from dataclasses import dataclass
# from enum import Enum

# class UserRole(Enum):
#     ADMIN = "admin"
#     USER = "user"

# @dataclass
# class User:
#     id: int
#     username: str
#     password_hash: str
#     role: UserRole = UserRole.USER

from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    username: str
    password: str

class TaskCreate(BaseModel):
    title: str
    description: str
    priority: int = 1
    due_date: str