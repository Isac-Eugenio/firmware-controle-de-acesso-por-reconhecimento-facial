from dataclasses import dataclass, field
from core.errors.camera_exceptions import CameraException
from services.ping_service import PingService
from core.config import app_config
from core.utils.api_utils import ApiUtils

@dataclass
class CameraModel:
    host: str
    port: int
    camera_id: str = field(init=False)
    full_host: str = field(init=False)
    status_online: bool = field(default=False, init=False)
    sizes: list = field(default_factory=lambda: [
        "96x96", "160x120", "176x144", "240x176", "240x240", "320x240",
        "400x296", "480x320", "640x480", "800x600", "1024x768", "1280x720",
        "1280x1024", "1600x1200"
    ])
    types: list = field(default_factory=lambda: ["BMP", "JPG", "MJPEG"])

    def __post_init__(self):
        _api_utils = ApiUtils()
        self.camera_id = _api_utils._generate_id()
        self.full_host = f"{self.host}:{self.port}"

    def status(self) -> bool:
        """Verifica se a câmera está online usando Ping"""
        try:
            is_online = PingService(self.host).ping()
            self.status_online = is_online
            return is_online
        except Exception as e:
            self.status_online = False
            raise CameraException(message=f"Erro ao verificar status da câmera: {str(e)}")
