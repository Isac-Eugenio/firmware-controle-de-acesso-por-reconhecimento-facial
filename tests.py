import asyncio
import hashlib
from controllers.user_controller import UserController
from core.config.app_config import (
    CameraConfig as Camera,
    DatabaseConfig,
    DatabaseTables,
    PerfisColumns,
)
from models.face_model import FaceModel
from models.login_model import LoginModel
from models.user_model import UserModel
from repository.camera_repository import CameraRepository
from repository.database_repository import DatabaseRepository, DATABASE_URL
from services.user_service import UserService
from services.face_service import FaceService
from core.utils.api_utils import ApiUtils


def _encoding_teste(float_value: float) -> str:
    zeros_float_str = ",".join([str(float_value)] * 128)
    return zeros_float_str


camera_rep = CameraRepository(Camera)
db_rep = DatabaseRepository()
face_model = FaceModel()
face_service = FaceService(camera_rep, face_model)

user_controller = UserController(face_service=face_service, database_repository=db_rep)


async def debug_async():
    form = {"id": "00000001", "senha": "@Isac1998", "email": "root.debug@gmail.com"}
    model = LoginModel.model_validate(form)
    User = UserService(face_service, db_rep)

    response = await User._verify_user_with_id(model)
    # print(dict(response.data))
    print(response)


async def debug_stream():
    # Preencha todos os campos relevantes de UserModel para um discente
    form_user = {
        "alias": "joao",
        "email": "joao@example.com",
        "nome": "João da Silva",
        "matricula": "2020202020202",
        "id": ApiUtils._generate_id(),
        "cpf": "233.233.233-99"
    }
    model_user = UserModel.model_validate(form_user)
    # LoginModel apenas com os campos necessários (sem senha)
    form_admin = {"id": "00000001", "email": "root.debug@gmail.com", "senha": "@Isac1998"}
    model_admin = LoginModel.model_validate(form_admin)

    # Testa o fluxo de registro
    async for resposta in user_controller.register(model_user, model_admin):
        print(resposta)


def debug():
    teste = {
        "email": "jao@gmail.com",
        "senha": "123456789",
        "permission_level": "administrador",
    }

    login = LoginModel.model_validate(teste)
    print(login)


if __name__ == "__main__":

    asyncio.run(debug_stream())
    # debug()
