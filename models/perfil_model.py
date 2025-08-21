from typing import Optional
from pydantic import BaseModel, Field
from models.user_model import UserModel, PermissionEnum


class PerfilModel(BaseModel):
    id: str
    nome: Optional[str] = Field(None, max_length=100)
    alias: Optional[str] = Field(None, max_length=11)
    email: Optional[str] = Field(None, max_length=255)
    matricula: Optional[str] = Field(None, max_length=255)
    icon_path: Optional[str] = Field(None, max_length=255)
    permission_level: PermissionEnum = PermissionEnum.DISCENTE

    @classmethod
    def from_user(cls, user: UserModel) -> "PerfilModel":
        # Retorna apenas dados seguros (sem cpf, senha, encodings, etc.)
        return cls(
            id=user.id,
            nome=user.nome,
            alias=user.alias,
            email=user.email,
            matricula=user.matricula,
            icon_path=user.icon_path,
            permission_level=user.permission_level,
        )
