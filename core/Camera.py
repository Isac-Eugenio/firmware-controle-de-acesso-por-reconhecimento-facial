from abc import ABC, abstractmethod
from .Ping import Ping  
import cv2

class Camera:
    def __init__(self, host, port): 
        self.host = host
        self.port = port
        self.full_host = f"{host}:{port}"
        self.status_online = self.status() 

    def __str__(self):
        return f'Camera(host={self.host}, port={self.port}, status={self.status_online})'
    
    def status(self):
        is_online = Ping(self.host).ping()
        self.status_online = is_online  
        return is_online
    
    @abstractmethod
    def get_frame(self, size: str, type: str):
        sizes = ["96x96", "160x120", "176x144", "240x176", "240x240", "320x240",
                "400x296", "480x320", "640x480", "800x600", "1024x768", "1280x720",
                "1280x1024", "1600x1200"]
        
        types = ["BMP","JPG","MJPEG"]

        if not self.status_online:
            print(f"Erro: Câmera em {self.full_host} está offline ! Verifique a conexão.")
            return None

        if size not in sizes:
            print(f"Erro: Tamanho '{size}' não suportado !. Tamanhos suportados: {sizes}")
            return None
        
        if type not in types:
            print(f"Erro: Tipo '{type}' não suportado !. Tipos suportados: {types}")
            return None
        

        try:
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

        except Exception as e:
            print(f"Erro ao capturar frame: {e}")
            return None
