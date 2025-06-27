import asyncio
import hashlib
from pydantic import ValidationError
from core.config.app_config import (
    CameraConfig as Camera,
    DatabaseConfig,
    DatabaseTables,
    PerfisColumns,
)
from models.baseuser_model import BaseUserModel
from models.face_model import FaceModel
from models.login_model import LoginModel
from models.camera_model import CameraModel
from models.query_model import QueryModel
from models.response_model import ResponseModel
from models.user_model import UserModel
from repository.camera_repository import CameraRepository
from repository.database_repository import DatabaseRepository, DATABASE_URL
from services.api_service import ApiService
from services.face_service import FaceService


def _encoding_teste(float_value: float) -> str:
    zeros_float_str = ",".join([str(float_value)] * 128)
    return zeros_float_str


admin_user = {
    "id": "ADM001",
    "nome": "Administrador Geral",
    "alias": "adminuser",
    "cpf": "123.456.789-00",
    "email": "admin@example.com",
    "matricula": "",
    "icon_path": "",
    "permission_level": "administrador",
    "senha": "admin1234",  # Deve ser uma senha válida

    # encodings está ausente
}


async def debug_async():

    camera_rep = CameraRepository(Camera)
    db_rep = DatabaseRepository()
    face_model = FaceModel()
    face_service = FaceService(camera_rep, face_model)
    api = ApiService(face_service, db_rep)

    novo_user = UserModel.model_validate(admin_user)
    novo_user.set_encoding(_encoding_teste(0.4))

    response = await api._insert_user(novo_user)

    print(response)

async def debug_stream():
    pass


def debug():
    novo_user = UserModel.model_validate(admin_user)
    novo_user.set_encoding(_encoding_teste(0.4))
    print(novo_user.model_dump())
    print(novo_user.verificar_senha("admin1234"))  # Deve retornar True

if __name__ == "__main__":

    asyncio.run(debug_async())
    #debug()
