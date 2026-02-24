from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoginLogBase(BaseModel):
    email: str
    ip_address: str
    success: bool

class LoginLogCreate(LoginLogBase):
    user_id: Optional[int] = None

class LoginLog(LoginLogBase):
    id: int
    timestamp: datetime
    user_id: Optional[int]

    class ConfigDict:
        from_attributes = True