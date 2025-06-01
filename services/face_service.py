from face_recognition import face_encodings, face_locations, compare_faces

from repository.camera_repository import CameraRepository
from core.config.app_config import config
from core.errors.face_exceptions import *
from core.errors.camera_exceptions import CameraException
from models.face_model import FaceModel

_HOST_CAMERA = config["hosts"]["camera"]
_PORT_CAMERA = config["ports"]["camera"]
_CONFIG_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CONFIG_CAMERA_FORMAT = config["details"]["camera"]["format"]

class FaceService:
    def __init__(self, camera_repository: CameraRepository, face_model: FaceModel):
        self.camera_repository = camera_repository
        self.face_model = face_model
        try:
            self._frame = camera_repository.get_frame(_CONFIG_CAMERA_RESOLUTION, _CONFIG_CAMERA_FORMAT)
        
        except CameraException as e:
            raise
        
    def get_face_locations(self):
        try:
            location = face_locations(self._frame)
            return location
            
        except Exception as e:
            raise FaceLocationError("Erro ao encontrar um rosto")

    def get_face_encodings(self):
        try:
            locations = self.get_face_locations()

            if not locations:
                raise FaceEncodingError("Nenhum rosto detectado")
                
            encodings = face_encodings(self._frame, locations)
            return encodings
        
        except FaceEncodingError as e:
            raise

        except Exception as e:
            raise FaceEncodingError("Erro ao gerar encoding do rosto") from e
    
    def get_first_face_encoding(self, location: tuple = None):
        try:
            if location is not None:
                if not isinstance(location, tuple):
                    raise FaceEncodingError("A localização fornecida não é uma tupla")
                
                encodings = face_encodings(self._frame, [location])

            else:
                encodings = self.get_face_encodings()

            if not encodings:
                raise FaceEncodingError("Nenhum encoding encontrado para o rosto")
            
            return encodings[0]
        
        except FaceEncodingError:
            raise
    
    def create_face_model(self) :
            try:
                locations = self.get_face_locations()
                if not locations:
                    raise FaceLocationError("Nenhum rosto detectado")
                
                self.face_model.location = locations[0]
                self.face_model.encoding = self.get_first_face_encoding(self.face_model.location)
            
            except (FaceEncodingError, FaceLocationError):
                raise 
    