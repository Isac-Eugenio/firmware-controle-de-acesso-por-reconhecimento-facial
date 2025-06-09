from typing import List, Tuple, Union, Optional
import numpy as np
from pydantic import BaseModel, field_validator, ValidationError, ConfigDict
from core.errors.face_exceptions import *

class FaceModel(BaseModel):
    encoding: Union[List[float], np.ndarray] = []
    location: Tuple[int, int, int, int] = ()

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # para aceitar np.ndarray
    )

    @field_validator("encoding", mode="before")
    @classmethod
    def validate_encoding(cls, v):
        if isinstance(v, str):
            return cls._encoding_array(v)
        elif isinstance(v, (list, np.ndarray)):
            if len(v) < 128:
                raise FaceEncodingError("Encoding vazio ou incompleto")
            return v
        else:
            raise FaceEncodingError("Tipo inválido para encoding")

    @field_validator("location")
    @classmethod
    def validate_location(cls, v):
        if not v or len(v) != 4:
            raise FaceLocationError("Location vazio ou inválido")
        return tuple(v)

    @staticmethod
    def _encoding_string(encoding: Union[List[float], np.ndarray]) -> str:
        try:
            if not isinstance(encoding, (list, np.ndarray)):
                raise ValueError("Esperado uma lista ou np.ndarray para codificação.")
            if encoding is None or len(encoding) < 128:
                raise FaceEncodingError("Encoding vazio ou incompleto")
            return ",".join(str(float(x)) for x in encoding)
        except (ValueError, TypeError) as e:
            raise FaceEncodingError("Erro ao converter encoding para string") from e

    @staticmethod
    def _encoding_array(encoding: str) -> np.ndarray:
        try:
            if not isinstance(encoding, str):
                raise ValueError("Esperado uma string para converter em array.")
            encoding_list = np.array([float(x.strip()) for x in encoding.split(',') if x.strip()])
            if len(encoding_list) < 128:
                raise FaceEncodingError("Encoding vazio ou incompleto")
            return encoding_list
        except (ValueError, TypeError) as e:
            raise FaceEncodingError("Erro ao converter string para encoding") from e

    def to_map(self, model: Optional['FaceModel'] = None) -> dict:
        try:
            if model is None:
                return {
                    "encoding": self.encoding.tolist() if isinstance(self.encoding, np.ndarray) else self.encoding,
                    "location": self.location
                }
            return {
                "encoding": self._encoding_string(model.encoding),
                "location": model.location
            }
        except Exception as e:
            raise FaceModelError("Erro ao converter FaceModel para mapa") from e
