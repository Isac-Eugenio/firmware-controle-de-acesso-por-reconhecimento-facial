from core.config.app_config import config
from dataclasses import dataclass, field
from typing import Optional, Dict
from enum import Enum
from models.face_model import FaceModel


class PermissionLevel(str, Enum):
    ADMIN = "admin"
    DISCENTE = "user"
    DOCENTE = "docente"


_COLUMNS_TABLE_PERFIS = config["details"]["database"]["tables"]["perfis"]["columns"]
_ENCODING_COLUMN = config["details"]["database"]["tables"]["perfis"]["encoding_column"]
_ALLOWED_FIELDS = _COLUMNS_TABLE_PERFIS + [_ENCODING_COLUMN]


@dataclass
class UserModel:
    nome: str = ""
    email: str = ""
    matricula: str = ""
    alias: str = ""
    cpf: str = ""
    id: str = ""
    encodings: str = ""
    permission_level: PermissionLevel = PermissionLevel.DISCENTE
    icon_path: str = ""

    _senha: str = field(default="", repr=False)
    _face_model: FaceModel = field(default_factory=FaceModel)

    @property
    def senha(self):
        raise AttributeError("A senha não pode ser acessada diretamente.")

    @senha.setter
    def senha(self, valor: str):
        self._senha = valor

    def to_dict(self) -> Dict[str, str]:

        result = {}
        for campo in _ALLOWED_FIELDS:
            valor = getattr(self, campo)

            if isinstance(valor, Enum):
                result[campo] = valor.value
            else:
                result[campo] = valor
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "UserModel":

        kwargs = {}
        for campo in _ALLOWED_FIELDS:
            if campo == "permission_level":
                kwargs[campo] = PermissionLevel(data.get(campo, "user"))
            else:
                kwargs[campo] = data.get(campo, "")

        return cls(**kwargs)
