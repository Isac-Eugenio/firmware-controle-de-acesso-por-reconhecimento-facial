from core.config.app_config import config
from core.errors.camera_exceptions import *
from models.camera_model import CameraModel
from repository.camera_repository import CameraRepository
from services.face_service import FaceUtils

_HOST_CAMERA = config["hosts"]["camera"]
_PORT_CAMERA = config["ports"]["camera"]
_CONFIG_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CONFIG_CAMERA_FORMAT = config["details"]["camera"]["format"]

class CameraController:
    def __init__(self):
        model = CameraModel(_HOST_CAMERA, _PORT_CAMERA)
        self.camera_repository = CameraRepository(model)
        self.fr = FaceUtils(self.get_frame)
        
        
    def get_frame(self, size: str, type: str):
        try:
            _frame = self.camera_repository.get_frame(size, type)
            return _frame

        except (CameraValueError, CameraConnectionError, CameraException) as e:
            raise CameraException(f"Controller: {e}")
    
    def _update_camera(self):
        try:
            _frame = self.get_frame(_CONFIG_CAMERA_RESOLUTION, _CONFIG_CAMERA_FORMAT)
            self.fr.update_frame(_frame)
            
        except CameraException as e:
            raise CameraException(f"controler: {e}")