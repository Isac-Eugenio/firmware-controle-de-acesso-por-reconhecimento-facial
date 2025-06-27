import hashlib
from typing import Optional, Union, Literal, List, get_args
import numpy as np
from pydantic import BaseModel, computed_field, field_validator, model_validator
from core.config.app_config import PerfisColumns
from core.errors.model_exception import ModelValueError
from models.face_model import FaceModel
import re

PermissionLiteral = Literal["administrador", "discente", "docente"]


def hash_sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


class BaseUserModel(BaseModel):
    nome: str = ""
    email: str = ""
    matricula: str = ""
    alias: str = ""
    cpf: str = ""
    id: str = ""
    permission_level: PermissionLiteral = "discente"
    icon_path: str = ""

    senha: str = ""  # pública e sempre será o hash
    _face_model: FaceModel = FaceModel()

    @model_validator(mode="before")
    def process_senha(cls, values):
        senha_raw = values.get("senha", "")
        if not senha_raw:
            raise ModelValueError("Senha não pode estar vazia.")

        # Se já estiver no formato de hash SHA-256
        if re.fullmatch(r"[0-9a-fA-F]{64}", senha_raw):
            values["senha"] = senha_raw.lower()
        else:
            if len(senha_raw) < 9:
                raise ModelValueError("Senha deve ter no mínimo 9 caracteres.")
            values["senha"] = hash_sha256(senha_raw)

        return values

    @field_validator("email")
    def check_email(cls, v):
        if v and "@" not in v:
            raise ModelValueError("Email inválido")
        return v

    @model_validator(mode="before")
    def check_permission_level(cls, values):
        pl = values.get("permission_level", "discente")
        if pl not in get_args(PermissionLiteral):
            raise ModelValueError(f"permission_level inválido: {pl}")
        values["permission_level"] = pl
        return values

    @classmethod
    def model_validate(cls, data: dict):
        return super().model_validate(data)

    def verificar_senha(self, senha: str) -> bool:
        return hash_sha256(senha) == self.senha

    @property
    def encodings(self) -> Optional[np.ndarray]:
        return self._face_model.encodings

    def set_encoding(self, encoding: Union[str, np.ndarray, List[float]]) -> None:
        if isinstance(encoding, str):
            encoding = self._face_model._encoding_array(encoding)

        if isinstance(encoding, list):
            encoding = np.array(encoding, dtype=float)

        if not isinstance(encoding, np.ndarray):
            raise ModelValueError("Encoding deve ser um np.ndarray ou uma string.")

        if encoding.dtype.kind not in ("f", "i"):
            raise ModelValueError("Encoding deve ser um array numérico (float ou int).")

        if encoding.size != 128:
            raise ModelValueError("Encoding deve conter exatamente 128 valores.")

        self._face_model.encoding = encoding
