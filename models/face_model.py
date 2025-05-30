from core.errors.face_exceptions import *
import numpy as np

class FaceModel:
    def __init__(self):
        self.encoding = []
        self.location = []

    @staticmethod
    def _encoding_string(encoding: list) -> str:
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

    def to_model(self, encoding: list, location: list) -> 'FaceModel':
        try:
            if encoding is None or len(encoding) < 128:
                raise FaceEncodingError("Encoding vazio ou incompleto")
            
            if not location:
                raise FaceLocationError("Location vazio")

            new_model = FaceModel()
            new_model.encoding = encoding
            new_model.location = location

            return new_model

        except Exception as e:
            raise FaceModelError("Erro ao montar FaceModel") from e

    def to_map(self, model: 'FaceModel' = None) -> dict:
        try:
            if model is None:
                return {
                "encoding": self.encoding,
                "location": self.location
                }
            
            return {
                "encoding": self._encoding_string(model.encoding),
                "location": model.location
            }
        except Exception as e:
            raise FaceModelError("Erro ao converter FaceModel para mapa") from e
