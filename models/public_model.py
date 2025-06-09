from core.config.app_config import PerfisColumns
from models.baseuser_model import UserModel
from dataclasses import dataclass, field
from typing import Dict
from core.config.app_config import config


@dataclass
class PublicUserModel(UserModel):
    _encoding: str = field(default="", repr=False)

    def to_dict(self) -> Dict[str, str]:
        result = {}
        for campo in PerfisColumns.PUBLIC:
            valor = getattr(self, campo)
            result[campo] = valor
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "PublicUserModel":
        kwargs = {campo: data.get(campo, "") for campo in PerfisColumns.PUBLIC}
        return cls(**kwargs)
