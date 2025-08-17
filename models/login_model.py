from pydantic import BaseModel
from core.commands.result import Result, Success, Failure
import re
from typing import Optional, get_args
from models.baseuser_model import PermissionLiteral
from core.utils.api_utils import ApiUtils

class LoginModel(BaseModel):
    email: str
    permission_level: PermissionLiteral = "administrador"
    alias: Optional[str] = None
    id: Optional[str] = None
    icon_path: Optional[str] = None
    senha: Optional[str] = None

    def validate_senha(self) -> Result[str, str]:
        per_level = self.permission_level.lower()
        senha_raw = self.senha or ""

        if per_level != "administrador":
            self.senha = None
            return Success(self.senha, log="Não administrador: senha ignorada", details="")

        if not senha_raw:
            return Failure("Senha não pode estar vazia para administradores", details="")

        if re.fullmatch(r"[0-9a-fA-F]{64}", senha_raw):
            self.senha = senha_raw.lower()
        else:
            if len(senha_raw) < 9:
                return Failure("Senha deve ter no mínimo 9 caracteres", details="")
            self.senha = ApiUtils._hash_sha256(senha_raw)

        return Success(self.senha, log="Senha validada com sucesso", details="")

    def validate_email(self) -> Result[str, str]:
        if self.email and "@" not in self.email:
            return Failure("Email inválido", details=f"Email fornecido: {self.email}")
        return Success(self.email, log="Email válido", details="")

    def validate_permission(self) -> Result[str, str]:
        if self.permission_level not in get_args(PermissionLiteral):
            return Failure(f"permission_level inválido: {self.permission_level}", details="")
        return Success(self.permission_level, log="Permission level válido", details="")
