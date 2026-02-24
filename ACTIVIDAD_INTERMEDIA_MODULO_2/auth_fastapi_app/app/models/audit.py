from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class LoginLog(Base):
    __tablename__ = "login_logs"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)  # Email intentado
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String)
    success = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # Opcional si el usuario existe