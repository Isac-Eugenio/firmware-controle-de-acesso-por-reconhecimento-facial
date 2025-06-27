from typing import Any, Optional
from pydantic import BaseModel

class ResponseModel(BaseModel):
    status: bool
    log: str
    error: Optional[bool] = False
    details: Optional[str] = None
    data: Optional[Any] = None
