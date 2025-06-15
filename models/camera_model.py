from core.errors.camera_exceptions import CameraException
from services.ping_service import PingService
from core.config.app_config import CameraConfig
from core.utils.api_utils import ApiUtils


class CameraModel:
    def __init__(self, config: CameraConfig):
        self.config = config
        self.host = config.host
        self.port = config.port
        self.resolution = config.resolution
        self.format = config.format

        self.available_resolutions = ["800x600", "1024x768", "1280x720"]
        self.available_formats = ["BMP", "JPG", "MJPEG"]

        self.camera_id = ApiUtils()._generate_id()
        self.full_host = f"http://{self.host}:{self.port}/{self.resolution}.{self.format}"
        self.status_online = False

    def status(self) -> bool:
        """Verifica se a câmera está online usando Ping"""
        try:
            is_online = PingService(self.host).ping()
            self.status_online = is_online
            return is_online
        except Exception as e:
            self.status_online = False
            raise CameraException(message=f"Erro ao verificar status da câmera: {str(e)}")
