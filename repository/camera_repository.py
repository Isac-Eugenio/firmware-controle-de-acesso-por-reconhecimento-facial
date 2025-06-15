from core.errors.camera_exceptions import *
from core.config.app_config import CameraConfig
from models.camera_model import CameraModel
import cv2

class CameraRepository(CameraModel):
    def __init__(self, config: CameraConfig):
        super().__init__(config)  # Primeiro inicializa os atributos herdados
        self.status_online = self.status()  # Agora pode usar os atributos

    def __str__(self):
        return f"Camera(host={self.host}, port={self.port}, status={self.status_online})"

    def get_frame(self):
        """Captura o frame da câmera"""
        self.status_online = self.status()
        if not self.status_online:
            raise CameraConnectionError(f"Câmera em {self.full_host} está offline! Verifique a conexão.")

        try:
            cap = cv2.VideoCapture(self.full_host)

            if not cap.isOpened():
                raise CameraConnectionError(f"Não foi possível abrir a câmera em {self.host}.")

            ret, frame = cap.read()
            cap.release()

            if not ret:
                raise CameraException(f"Não foi possível capturar o frame da câmera em {self.host}.")

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame

        except (CameraValueError, CameraConnectionError, CameraException):
            raise

        except Exception as e:
            raise CameraException(str(e))
