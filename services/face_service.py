import face_recognition as fr
import numpy as np
from core.errors.face_exceptions import FaceRecognitionError, FaceServiceError


class FaceUtils:
    def __init__(self, frame=None):
        self.frame = frame
        self._face_locations = None
        self._face_encodings = None

    def locations(self):
        """Retorna a localização das faces no frame."""
        if self._face_locations is not None:
            return self._face_locations  # Retorna cache se já foi calculado
        
        try:
            self._face_locations = fr.face_locations(self.frame)
        except Exception as e:
            raise FaceRecognitionError("Erro ao detectar localizações faciais", str(e))
        
        return self._face_locations
    
    def encodings(self):
        if self._face_encodings is not None:
            return self._face_encodings
        
        try:
            self._face_encodings = fr.face_encodings(self.frame, self._face_locations)
        except Exception as e:
            raise FaceRecognitionError("Erro ao gerar os encodings", str(e))
        
        return {"encodings": self._face_encodings, "locations": self._face_locations}
        
    def update_frame(self, new_frame):
        """Atualiza o frame para permitir novo processamento."""
        self.frame = new_frame
        self._face_locations = None  # Limpa o cache de localizações
        self._face_encodings = None  # Limpa o cache de encodings

    def compare_faces(self, known_face_encodings, face_encoding_to_check, trust):
        _trust = -(trust/100)+1

        try:

            results = fr.compare_faces(known_face_encodings, face_encoding_to_check, tolerance=_trust)
        except Exception as e:
            raise FaceRecognitionError("Erro ao comparar rostos", str(e))
        
        return results
