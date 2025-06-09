from typing import List, Optional
from pydantic import BaseModel, PrivateAttr, field_validator, model_validator
from enum import Enum
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
    
    _senha: str = PrivateAttr(default="")
    _face_model: FaceModel = PrivateAttr(default_factory=FaceModel)

    @property
    def encoding(self) -> Optional[List[float]]:
        return self._face_model.encoding

    def set_encoding(self, encoding: list[float] | str) -> None:
        if isinstance(encoding, str):
            encoding = self._face_model._encoding_array(encoding)

        if not isinstance(encoding, list) or not all(isinstance(x, (float, int)) for x in encoding):
            raise ModelValueError("Encoding deve ser uma lista de números (float ou int).")

        self._face_model.encoding = encoding


    @property
    def senha(self):
        raise ModelAttributeError("A senha não pode ser acessada diretamente.")

    @senha.setter
    def senha(self, valor: str):
        self._senha = valor

    def _get_senha(self) -> str:
        """
        Método protegido para obter a senha.
        Permite acesso apenas para instâncias da própria classe ou subclasses.
        """
        caller_self = None
        # Tenta obter o objeto que chamou este método
        try:
            caller_self = inspect.stack()[1].frame.f_locals.get('self', None)
        except Exception:
            pass

        if caller_self and isinstance(caller_self, BaseUserModel):
            return self._senha
        raise ModelAttributeError("A senha não pode ser acessada diretamente por esta instância.")

    @field_validator('email')
    def check_email(cls, v):
        if v and '@' not in v:
            raise ModelValueError("Email inválido")
        return v

    @model_validator(mode='before')
    def check_permission_level(cls, values):
        pl = values.get('permission_level')
        if pl is None:
            values['permission_level'] = PermissionLevel.DISCENTE
        elif isinstance(pl, str):
            try:
                values['permission_level'] = PermissionLevel(pl)
            except ValueError:
                raise ModelValueError(f"permission_level inválido: {pl}")
        elif not isinstance(pl, PermissionLevel):
            raise ModelValueError(f"permission_level inválido: {pl}")
        return values

    class Config:
        underscore_attrs_are_private = True
        allow_mutation = True
