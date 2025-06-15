from typing import Optional, List, Union
import numpy as np
from pydantic import BaseModel, PrivateAttr, field_validator, model_validator
from enum import Enum
from passlib.hash import bcrypt
from core.config.app_config import PerfisColumns
from core.errors.model_exception import ModelAttributeError, ModelValueError
from models.face_model import FaceModel
import inspect


class PermissionLevel(str, Enum):
    ADMINISTRADOR = "administrador"
    DISCENTE = "discente"
    DOCENTE = "docente"


class BaseUserModel(BaseModel):
    nome: str = ""
    email: str = ""
    matricula: str = ""
    alias: str = ""
    cpf: str = ""
    id: str = ""
    permission_level: PermissionLevel = PermissionLevel.DISCENTE
    icon_path: str = ""

    # campo senha temporário só para entrada de texto puro na criação
    senha: Optional[str] = None

    # atributos privados
    _senha_hash: str = PrivateAttr("")
    _face_model: FaceModel = PrivateAttr(default_factory=FaceModel)

    @model_validator(mode="before")
    def process_senha(cls, values):
        senha_raw = values.get("senha")
        if senha_raw:
            if len(senha_raw) < 9:
                raise ModelValueError("Senha deve ter no mínimo 9 caracteres")
            # Hash da senha já aqui
            values["_senha_hash"] = bcrypt.hash(senha_raw)
            # Remove senha em texto puro para não ficar no modelo final
            values["senha"] = None
        else:
            values["_senha_hash"] = ""
        return values

    # email validation
    @field_validator("email")
    def check_email(cls, v):
        if v and "@" not in v:
            raise ModelValueError("Email inválido")
        return v

    @model_validator(mode="before")
    def check_permission_level(cls, values):
        pl = values.get("permission_level")
        if pl is None:
            values["permission_level"] = PermissionLevel.DISCENTE
        elif isinstance(pl, str):
            try:
                values["permission_level"] = PermissionLevel(pl)
            except ValueError:
                raise ModelValueError(f"permission_level inválido: {pl}")
        elif not isinstance(pl, PermissionLevel):
            raise ModelValueError(f"permission_level inválido: {pl}")
        return values

    @classmethod
    def model_validate(cls, data: dict): 
        senha = data.pop(PerfisColumns().password)
        obj = super().model_validate(data)
        obj._senha_hash = bcrypt.hash(senha)
        return obj

    @property
    def senha(self):
        # só quem herda pode acessar o hash
        caller_self = None
        try:
            caller_self = inspect.stack()[1].frame.f_locals.get("self", None)
        except Exception:
            pass
        if caller_self and isinstance(caller_self, BaseUserModel):
            return self._senha_hash
        raise ModelAttributeError("A senha não pode ser acessada diretamente.")

    def verificar_senha(self, senha: str) -> bool:
        return bcrypt.verify(senha, self._senha_hash)

    # Email Setter seguro
    def set_email(self, email: str) -> None:
        if "@" not in email:
            raise ModelValueError("Email inválido")
        self.email = email


    @property
    def encoding(self) -> Optional[np.ndarray]:
        return self._face_model.encoding

    def set_encoding(self, encoding: Union[str, np.ndarray, list[float]]) -> None:
        if isinstance(encoding, str):
            encoding = self._face_model._encoding_array(encoding)  # já retorna np.ndarray

        # Se for lista, converte para np.ndarray
        if isinstance(encoding, list):
            encoding = np.array(encoding, dtype=float)

        # Agora garante que é np.ndarray com float
        if not isinstance(encoding, np.ndarray):
            raise ModelValueError("Encoding deve ser um np.ndarray ou uma string.")

        if encoding.dtype.kind not in ("f", "i"):  # float ou int
            raise ModelValueError("Encoding deve ser um array numérico (float ou int).")

        if encoding.size != 128:
            raise ModelValueError("Encoding deve conter exatamente 128 valores.")

        self._face_model.encoding = encoding
