from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class ResponseModel:
    status: bool
    log: str
    details: Optional[str] = None
    data: Optional[Any] = None
    error: Optional[bool] = False
    