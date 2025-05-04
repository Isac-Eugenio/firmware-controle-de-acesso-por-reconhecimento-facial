import face_recognition as fr
from .Camera import Camera

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
            print(f"Erro ao detectar localizações faciais: {e}")
            self._face_locations = []

        return self._face_locations
    
    def encodings(self):
        """Retorna os encodings das faces no frame."""
        face_locations = self.locations()
        
        if not face_locations:
            return {"message": "Nenhum rosto encontrado!", "status": False, "encodings":[], "locations": []}
        
        try:
            # Só recalcula os encodings se as localizações mudaram
            if self._face_encodings is None or face_locations != self._face_locations:
                self._face_encodings = fr.face_encodings(self.frame, face_locations)
            
            if not self._face_encodings:
                return {"message": "Nenhum encoding gerado!", "status": False, "encodings": []}
        except Exception as e:
            return {"message": f"Erro ao gerar os encodings: {e}", "status": False, "encodings": []}
        
        return {"message": "Encoding gerado com sucesso!", "status": True, "encodings": self._face_encodings, "locations": face_locations}
    
    def update_frame(self, new_frame):
        """Atualiza o frame para permitir novo processamento."""
        self.frame = new_frame
        self._face_locations = None  # Limpa o cache de localizações
        self._face_encodings = None  # Limpa o cache de encodings
        print("Frame atualizado com sucesso.")

    def compare_faces(known_face_encodings, face_encoding_to_check, trust):
        
        results = fr.compare_faces(known_face_encodings, face_encoding_to_check)

        return results