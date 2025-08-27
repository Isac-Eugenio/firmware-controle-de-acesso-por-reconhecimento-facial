import asyncio
from core.commands.result import *
from models.face_model import FaceModel
from models.perfil_model import PerfilModel
from services.face_service import FaceService


class FaceRepository:

    def __init__(self, face_service: FaceService, face_model: FaceModel):
        self.face_service = face_service
        self.face_model = face_model

    def match_face_to_profiles(
        self,
        list_profiles: list[PerfilModel],
        face_encoding: list[float],
        tolerance: int = 60,
    ) -> Result[PerfilModel, str]:
        list_encodings = []

        for perfil in list_profiles:
            list_encodings.append(perfil.encodings)

        try:
            list_distance = [
                self._distance_percent(enc)
                for enc in self.face_service.fr.face_distance(
                    list_encodings, face_encoding
                )
            ]

            for i, perfil in enumerate(list_profiles):
                if list_distance[i] >= tolerance:
                    return Success(
                        perfil,
                        log=f"Rosto reconhecido como {perfil.nome} com {list_distance[i]:.2f}% de similaridade",
                    )
            return Failure(
                "Rosto não reconhecido", details="Nenhum perfil correspondente"
            )

        except Exception as e:
            return Failure("Erro ao reconhecer rosto", details=str(e))

    async def match_face_to_profiles_async(
        self,
        list_profiles: list[PerfilModel],
        face_encoding: list[float],
        tolerance: int = 60,
    ) -> Result[FaceModel, str]:

        loop = asyncio.get_running_loop()

        return await loop.run_in_executor(
            None,
            lambda: self.match_face_to_profiles(
                list_profiles, face_encoding, tolerance
            ),
        )

    def _distance_percent(self, distance: float) -> float:
        return ((-distance) + 1) * 100
