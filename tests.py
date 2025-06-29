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
from models.query_model import QueryModel
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
    pass


async def debug_stream():
    form_admin = {
        "id": "00000001",
        "email": "root.debug@gmail.com",
        "senha": "@Isac1998",
    }
    model_admin = LoginModel.model_validate(form_admin)

    form_user = {"id": "09027797"}

    form_novo = {"email": "joaosilva2@gmail.com"}

    model_user = UserModel.model_validate(form_user)

    model_novo = UserModel.model_validate(form_novo)

    tasks = [
        (
            "Inserir Usuario",
            lambda: user_controller.update(
                model_admin,
                model_user,
                model_novo
            ),
        )
    ]

    async for resp in ApiUtils._execute_task(tasks, db_rep):
        print(resp)


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
