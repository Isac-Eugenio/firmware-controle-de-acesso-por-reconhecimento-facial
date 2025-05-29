
import cv2
from ..services.ping_service import Ping
from models.camera_model import CameraModel

class CameraRepository:
    def __init__(self):
        model = CameraModel()
        self.host = model.host
        self.port = model.port
        self.sizes = model.sizes
        self.types = model.types
        self.full_host = model.full_host


    def __str__(self):
        return f'Camera(host={self.host}, port={self.port}, status={self.status_online})'

    def validate_size_and_type(self, size, type):
   

        if size not in self.sizes:
            raise ValueError(f"Tamanho '{size}' não suportado! Tamanhos suportados: {self.sizes}")
        
        if type not in self.types:
            raise ValueError(f"Tipo '{type}' não suportado! Tipos suportados: {self.types}")
        
        return True

    def get_frame(self, size: str, type: str):
        """Captura o frame da câmera"""
        if not self.status_online:
            print(f"Erro: Câmera em {self.full_host} está offline! Verifique a conexão.")
            return None

        try:
            self.validate_size_and_type(size, type)

            _host_camera = f"http://{self.full_host}/{size}.{type.lower()}"
            cap = cv2.VideoCapture(_host_camera)

            if not cap.isOpened():
                print(f"Erro: Não foi possível abrir a câmera em {self.full_host}.")
                return None
            
            ret, frame = cap.read()
            cap.release()

            if not ret:
                print(f"Erro: Não foi possível capturar o frame da câmera em {self.full_host}.")
                return None

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return frame

        except ValueError as ve:
            raise Exception(ve)
          
        except Exception as e:
            raise Exception(e)
