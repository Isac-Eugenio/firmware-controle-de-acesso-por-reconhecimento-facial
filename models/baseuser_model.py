import hashlib
from typing import Optional, Union, Literal, List, get_args
import numpy as np
from pydantic import BaseModel, computed_field, field_validator, model_validator
from core.config.app_config import PerfisColumns
from core.errors.model_exception import ModelValueError
from core.utils.api_utils import ApiUtils
from models.face_model import FaceModel
import re

PermissionLiteral = Literal["administrador", "discente", "docente"]
ApiUtils = ApiUtils()

class BaseUserModel(BaseModel):
    nome: str = ""
    email: str = ""
    matricula: Optional[str] = None
    alias: str = ""
    cpf: str = ""
    id: str = ""
    permission_level: PermissionLiteral = "discente"
    icon_path: Optional[str] = None
    encodings: str = ""
    senha: Optional[str] = None 
    _face_model: FaceModel = FaceModel()

    @model_validator(mode="before")
    def process_senha(cls, values):
        senha_raw = values.get("senha", "")
        per_level = values.get("permission_level", "").lower()

        # Se NÃO for administrador, ignora a senha (zera ou None)
        if per_level != "administrador":
            values["senha"] = None
            return values

        # Se for administrador, senha não pode estar vazia
        if not senha_raw:
            raise ModelValueError("Senha não pode estar vazia para administradores.")

        # Se senha já for hash SHA-256 (64 hex chars)
        if re.fullmatch(r"[0-9a-fA-F]{64}", senha_raw):
            values["senha"] = senha_raw.lower()
        else:
            # Senha raw, precisa ter no mínimo 9 chars para hash
            if len(senha_raw) < 9:
                raise ModelValueError("Senha deve ter no mínimo 9 caracteres.")
            values["senha"] = ApiUtils._hash_sha256(senha_raw)

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

    """  @classmethod
    def model_validate(cls, data: dict):
        return super().model_validate(data) """

    def verificar_senha(self, senha: str | bytes) -> bool:
        """
        Verifica se a senha fornecida corresponde à armazenada.
        Aceita apenas senhas já hasheadas (64 hex chars).
        """
        # Converte bytes para string
        if isinstance(senha, bytes):
            try:
                senha = senha.decode("utf-8")
            except UnicodeDecodeError:
                return False

        if not isinstance(senha, str):
            return False

        # Valida se é um hash SHA-256 válido (64 caracteres hexadecimais)
        if len(senha) != 64:
            return False
        try:
            int(senha, 16)
        except ValueError:
            return False

        # Compara com a senha armazenada
        return senha.lower() == (self.senha or "").lower()

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

        self._face_model.encodings = encoding
        self.encodings = self._face_model._encoding_string(encoding)
