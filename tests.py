import asyncio
import hashlib
from core.config.app_config import (
    CameraConfig as Camera,
    DatabaseConfig,
    DatabaseTables,
    PerfisColumns,
)
from models.face_model import FaceModel
from models.user_model import UserModel
from repository.camera_repository import CameraRepository
from repository.database_repository import DatabaseRepository, DATABASE_URL
from services.api_service import ApiService
from services.face_service import FaceService
from core.utils.api_utils import ApiUtils


def _encoding_teste(float_value: float) -> str:
    zeros_float_str = ",".join([str(float_value)] * 128)
    return zeros_float_str


api_utils = ApiUtils()

admin_user = {
  "id":"77543246"
}
teste_user = {
    "email":"joao1@example.com"
}


async def debug_async():

    camera_rep = CameraRepository(Camera)
    db_rep = DatabaseRepository()
    face_model = FaceModel()
    face_service = FaceService(camera_rep, face_model)
    api = ApiService(face_service, db_rep)

    novo_user = UserModel()
    now_user = UserModel()
    now_user.email = "joaosilva@example.com"
    novo_user.id = "77543246"


    response = await api._update_user(novo_user, now_user)
    print(response)


async def debug_stream():
    pass


def debug():
    novo_user = UserModel.model_validate(admin_user)
    novo_user.set_encoding(_encoding_teste(0.4))
    print(novo_user.model_dump())
    print(novo_user.verificar_senha("admin1234"))


if __name__ == "__main__":

    asyncio.run(debug_async())
    # debug()
