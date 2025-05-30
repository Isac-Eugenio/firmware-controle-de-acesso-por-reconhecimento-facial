from core.errors.camera_exceptions import *
from services.ping_service import PingService as Ping
from models.camera_model import CameraModel
import cv2

class CameraRepository:
    def __init__(self, model: CameraModel):
        self.host = model.host
        self.port = model.port
        self.sizes = model.sizes
        self.types = model.types
        self.full_host = model.full_host
        self.status_online = model.status()

    def __str__(self):
        return f'Camera(host={self.host}, port={self.port}, status={self.status_online})'

    def validate_size_and_type(self, size, type):
        if size not in self.sizes:
            raise CameraValueError(f"Tamanho '{size}' não suportado! Tamanhos suportados: {self.sizes}")
        if type not in self.types:
            raise CameraValueError(f"Tipo '{type}' não suportado! Tipos suportados: {self.types}")
        return True

    def get_frame(self, size: str, type: str):
        """Captura o frame da câmera"""
        if not self.status_online:
            raise CameraConnectionError(f"Câmera em {self.full_host} está offline! Verifique a conexão.")

        try:
            self.validate_size_and_type(size, type.upper())
            _host_camera = f"http://{self.full_host}/{size}.{type.lower()}"
            cap = cv2.VideoCapture(_host_camera)

            if not cap.isOpened():
                raise CameraConnectionError(f"Não foi possível abrir a câmera em {self.full_host}.")

            ret, frame = cap.read()
            cap.release()

            if not ret:
                raise CameraException(f"Não foi possível capturar o frame da câmera em {self.full_host}.")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame

        except (CameraValueError, CameraConnectionError, CameraException):
            raise 
        
        except Exception as e:
            raise CameraException(str(e))
