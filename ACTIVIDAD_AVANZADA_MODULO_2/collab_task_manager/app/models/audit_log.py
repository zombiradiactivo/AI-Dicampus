from dataclasses import dataclass
from datetime import datetime

@dataclass
class AuditEntry:
    user_id: int
    action: str  # e.g., "LOGIN", "DELETE_TASK"
    resource: str
    timestamp: datetime
    ip_address: str = "0.0.0.0"