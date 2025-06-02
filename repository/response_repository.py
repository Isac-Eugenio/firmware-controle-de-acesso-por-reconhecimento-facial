from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class RepositoryResponse:
    status: bool
    log: str
    data: Optional[Any] = None
    error: Optional[str] = None