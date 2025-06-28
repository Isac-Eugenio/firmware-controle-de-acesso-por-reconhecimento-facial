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
from services.api_service import ApiService
from services.face_service import FaceService
from core.utils.api_utils import ApiUtils


def _encoding_teste(float_value: float) -> str:
    zeros_float_str = ",".join([str(float_value)] * 128)
    return zeros_float_str


admin_user = {
   "alias":"joao",
   "email":"joao@example.com",
   "nome":"João da Silva",
   "permission_level": "discente",
   "matricula": "2020202020202",

}

camera_rep = CameraRepository(Camera)
db_rep = DatabaseRepository()
face_model = FaceModel()
face_service = FaceService(camera_rep, face_model)

user_controller = UserController(face_service=face_service, database_repository=db_rep)


async def debug_async():
    teste = {
        "email": "root.debug@gmail.com",
        "senha": "@Isac1998"
    }
    model = LoginModel.model_validate(teste)
    api = ApiService(face_service, db_rep)

    response = await api._login_user(model)
    print(dict(response.data))
    print(response)


async def debug_stream():
    admin = UserModel()
    admin.id = "20109807"

    form = {
        "email":"root.debug@gmail.com",
        "senha":"@Isac1998"
    }

    model = LoginModel.model_validate(form)
    async for resposta in user_controller.login(model):
        res = resposta
        print(res)

        


def debug():
    teste = {
        "email": "jao@gmail.com",
        "senha":"123456789",
        "permission_level": "administrador"
    }

    login = LoginModel.model_validate(teste)
    print(login)

if __name__ == "__main__":

    asyncio.run(debug_stream())
    #debug()
