from typing import Any
from numpy import dtype, floating, integer, ndarray
from core.commands.command import Command
from core.commands.result import Failure, Result, Success
from core.config.app_config import CameraConfig
from models.camera_model import CameraModel
import cv2


class CameraRepository(CameraModel):
    def __init__(self, config: CameraConfig):
        super().__init__(config)
        self.command = Command()
        
    def __str__(self):
        return (
            f"Camera(host={self.host}, port={self.port}, status={self.status_online})"
        )

    def release(self):
        if self.cap.isOpened():
            self.cap.release()

    def _get_frame(
        self,
    ) -> Result[cv2.Mat | ndarray[Any, dtype[integer[Any] | floating[Any]]], str]:
        self.status_online = self.status()

        if not self.status_online:
            return Failure(f"Camera no host {self.full_host} está offline")

        cap = cv2.VideoCapture(self.full_host)

        if not cap.isOpened():
            return Failure(f"Não foi possível abrir a câmera em {self.host}.")

        ret, frame = cap.read()
        cap.release()

        if not ret:
            return Failure(
                f"Não foi possível capturar o frame da câmera em {self.host}."
            )

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Success(frame)

    def get_frame(self) -> Result[cv2.Mat | ndarray[Any, dtype[integer[Any] | floating[Any]]], str]:
        result = self.command.execute(self._get_frame)
        return result
