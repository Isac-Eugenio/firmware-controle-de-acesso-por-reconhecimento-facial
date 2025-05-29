from core.errors.camera_exceptions import CameraException
from services.ping_service import PingService
from core.config import config
from utils.api_utils import ApiUtils

class CameraModel:
    def __init__(self, host, port):
        self._host = host
        self._port = port
        self.camera_id = ApiUtils._generate_id()
       
        self.sizes = ["96x96", "160x120", "176x144", "240x176", "240x240", "320x240",
                      "400x296", "480x320", "640x480", "800x600", "1024x768", "1280x720",
                      "1280x1024", "1600x1200"]
        
        self.types = ["BMP", "JPG", "MJPEG"]
        self.full_host = f"{self._host}:{self._port}"

    def status(self):
        """Verifica se a câmera está online usando Ping"""
        try:
            is_online = PingService(self.host).ping()
            self.status_online = is_online
            return is_online
        except Exception as e:
            self.status_online = False
            raise CameraException(f"Erro ao verificar status da câmera: {str(e)}")
        