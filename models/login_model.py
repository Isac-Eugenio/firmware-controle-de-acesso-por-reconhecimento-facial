import re
from typing import Optional, get_args
from pydantic import BaseModel, Field, field_validator, model_validator
from core.errors.model_exception import ModelValueError
from core.utils.api_utils import ApiUtils
from models.baseuser_model import PermissionLiteral

class LoginModel(BaseModel):
    email: str
    permission_level: PermissionLiteral = Field(default="administrador")
    alias: Optional[str] = None
    id: Optional[str] = None
    icon_path: Optional[str] = None
    senha: Optional[str] = None 

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
    
    @model_validator(mode="before")
    @classmethod
    def force_admin(cls, values: dict):
        values["permission_level"] = "administrador"

        if values["permission_level"] not in get_args(PermissionLiteral):
            raise ModelValueError(f"permission_level inválido: {values['permission_level']}")
        
        return values

