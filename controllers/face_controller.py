from models.face_model import FaceModel
from repository.camera_repository import CameraRepository
from core.config.app_config import config

_HOST_CAMERA = config["hosts"]["camera"]
_PORT_CAMERA = config["ports"]["camera"]
_CONFIG_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CONFIG_CAMERA_FORMAT = config["details"]["camera"]["format"]

class FaceController:
    def __init__(self, camera_repository: CameraRepository, face_model: FaceModel):
        self.camera_repository = camera_repository
        self.face_model = face_model
        
        self._frame = camera_repository.get_frame(_CONFIG_CAMERA_RESOLUTION, _CONFIG_CAMERA_FORMAT)

    def update_location():
        