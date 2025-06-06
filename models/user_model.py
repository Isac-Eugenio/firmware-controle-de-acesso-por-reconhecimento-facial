from dataclasses import dataclass, field
from typing import Optional
from models.face_model import FaceModel


@dataclass
class UserModel:
    nome: str = ""
    email: str = ""
    matricula: str = ""
    alias: str = ""
    cpf: str = ""
    id: str = ""
    _senha: str = field(default="", repr=False)
    _face_model: FaceModel = field(default_factory=FaceModel)

    @property
    def senha(self):
        raise AttributeError("A senha não pode ser acessada diretamente.")

    @senha.setter
    def senha(self, valor: str):
        self._senha = valor

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "matricula": self.matricula,
            "alias": self.alias,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserModel":
        obj = cls(
            nome=data.get("nome", ""),
            email=data.get("email", ""),
            matricula=data.get("matricula", ""),
            alias=data.get("alias", ""),
            id=data.get("id", ""),
        )
        return obj
