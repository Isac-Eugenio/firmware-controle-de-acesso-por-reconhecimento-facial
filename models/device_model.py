from dataclasses import Field
from typing import Optional

from pydantic import BaseModel


class DeviceModel(BaseModel):
    mac: Optional[str] = None
    local: Optional[str] = None
