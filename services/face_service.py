from typing import Any
from face_recognition import face_encodings, face_locations

from core.commands.result import Failure, Result, Success
from repository.camera_repository import CameraRepository
from models.face_model import FaceModel


class FaceService:
    def __init__(self, camera_repository: CameraRepository):
        self.camera_repository = camera_repository
        self._frame = camera_repository.get_frame()  # Result esperado aqui

    def get_face_locations(self) -> Result[list[tuple[int, Any, Any, int]], str]:
        """Detecta todas as localizações de rostos no frame atual."""
        if self._frame.is_failure:
            return Failure("Erro ao obter o frame da câmera", details=self._frame.value)

        try:
            locations = face_locations(self._frame.value)
            if not locations:
                return Failure("Nenhum rosto encontrado")
            return Success(locations, log="Rostos encontrados com sucesso")
        except Exception as e:
            return Failure("Erro inesperado ao detectar rostos", details=str(e))

    def get_face_encodings(self) -> Result[list[Any], str]:
        """Gera encodings para todos os rostos encontrados no frame atual."""
        if self._frame.is_failure:
            return Failure("Erro ao obter o frame da câmera", details=self._frame.value)

        locations_result = self.get_face_locations()
        if locations_result.is_failure:
            return Failure("Erro ao encontrar rostos", details=locations_result.value)

        try:
            encodings = face_encodings(self._frame.value, locations_result.value)
            if not encodings:
                return Failure("Nenhum encoding gerado")
            return Success(encodings, log="Encodings gerados com sucesso")
        except Exception as e:
            return Failure("Erro inesperado ao gerar encodings", details=str(e))

    def get_first_face_encoding(self) -> Result[Any, str]:
        """Retorna apenas o primeiro encoding encontrado no frame."""
        encodings_result = self.get_face_encodings()
        if encodings_result.is_failure:
            return Failure("Erro ao obter encodings", details=encodings_result.value)

        first_encoding = encodings_result.value[0]
        return Success(first_encoding, log="Primeiro encoding obtido com sucesso")

    def create_face_model(self) -> Result[FaceModel, str]:
        """Cria e valida um FaceModel com a primeira face encontrada no frame."""
        locations_result = self.get_face_locations()
        if locations_result.is_failure:
            return Failure("Erro ao obter localização do rosto", details=locations_result.value)

        encodings_result = self.get_first_face_encoding()
        if encodings_result.is_failure:
            return Failure("Erro ao obter encoding do rosto", details=encodings_result.value)

        try:
            # Usa Pydantic para validar
            face_model = FaceModel(
                location=locations_result.value[0],
                encodings=encodings_result.value,
                frame=self._frame.value
            )
            return Success(face_model, log="FaceModel criado com sucesso")
        except Exception as e:
            return Failure("Erro ao validar FaceModel", details=str(e))
