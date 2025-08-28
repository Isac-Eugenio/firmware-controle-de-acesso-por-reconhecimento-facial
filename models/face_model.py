from typing import Any, List, Tuple, Union, Optional
import cv2
import numpy as np
from pydantic import BaseModel, field_validator, ConfigDict
from core.commands.result import Result, Success, Failure


class FaceModel(BaseModel):
    encodings: Union[List[float]] = []
    location: Tuple[int, int, int, int] = ()

    frame: cv2.Mat | np.ndarray[Any, np.dtype[np.integer[Any] | np.floating[Any]]] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # permite np.ndarray no Pydantic
    )

    # -----------------
    # VALIDADORES
    # ------------------------
    
    @field_validator("encodings", mode="before")
    @classmethod
    def validate_encoding(cls, v) -> Union[List[float], np.ndarray]:
        res = cls._validate_encoding(v)
        if res.is_failure:
            raise ValueError(res.details or "Encoding inválido")
        return res.value

    @field_validator("location")
    @classmethod
    def validate_location(cls, v) -> Tuple[int, int, int, int]:
        if not v or len(v) != 4:
            raise ValueError("Location vazio ou inválido")
        return tuple(v)

    # ------------------------
    # HELPERS DE ENCODING
    # ------------------------
    @staticmethod
    def _validate_encoding(encoding: Union[str, List[float], np.ndarray]) -> Result[Union[List[float], np.ndarray], str]:
        try:
            if isinstance(encoding, str):
                arr = np.array([float(x.strip()) for x in encoding.split(",") if x.strip()])
                if arr.size < 128:
                    return Failure("Encoding incompleto", details=f"Tamanho recebido: {arr.size}")
                return Success(arr, log="Encoding convertido de string", details=f"Tamanho: {arr.size}")

            if isinstance(encoding, (list, np.ndarray)):
                length = len(encoding)
                if length < 128:
                    return Failure("Encoding incompleto", details=f"Tamanho recebido: {length}")
                return Success(np.array(encoding), log="Encoding válido", details=f"Tamanho: {length}")

            return Failure("Tipo inválido para encoding", details=f"Tipo: {type(encoding)}")

        except Exception as e:
            return Failure("Erro ao validar encoding", details=str(e))

    @staticmethod
    def _encoding_string(encoding: Union[List[float], np.ndarray]) -> Result[str, str]:
        try:
            val_res = FaceModel._validate_encoding(encoding)
            if val_res.is_failure:
                return val_res
            arr = np.array(val_res.value)
            s = ",".join(str(float(x)) for x in arr)
            return Success(s, log="Encoding convertido para string", details=f"Tamanho: {arr.size}")
        except Exception as e:
            return Failure("Erro ao converter encoding para string", details=str(e))

    @staticmethod
    def _encoding_array(encoding: str) -> Result[np.ndarray, str]:
        return FaceModel._validate_encoding(encoding)

    # ------------------------
    # SERIALIZAÇÃO
    # ------------------------
    def to_map(self, model: Optional["FaceModel"] = None, as_string: bool = False) -> Result[dict, str]:
        """
        Converte o modelo para dict.
        - Se as_string=True → encodings como string serializada
        - Se False → encodings como lista
        """
        try:
            target = model or self
            if as_string:
                enc_res = self._encoding_string(target.encodings)
                if enc_res.is_failure:
                    return enc_res
                encodings_out = enc_res.value
            else:
                encodings_out = (
                    target.encodings.tolist()
                    if isinstance(target.encodings, np.ndarray)
                    else target.encodings
                )

            return Success(
                {
                    "encodings": encodings_out,
                    "location": target.location,
                },
                log="FaceModel convertido para dict",
                details=f"Encodings serializado como {'string' if as_string else 'lista'}"
            )
        except Exception as e:
            return Failure("Erro ao converter FaceModel para dict", details=str(e))
