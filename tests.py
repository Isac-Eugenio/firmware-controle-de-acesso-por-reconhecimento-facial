import asyncio
import hashlib
from controllers.api_controller import ApiController
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


admin_user = {
   "alias":"joao",
   "email":"joao@example.com",
   "nome":"João da Silva",
   "permission_level": "discente",
   "matricula": "2020202020202",
   "cpf": "202.202.222-77",
   "id": ApiUtils._generate_id()

}

camera_rep = CameraRepository(Camera)
db_rep = DatabaseRepository()
face_model = FaceModel()
face_service = FaceService(camera_rep, face_model)

api_controller = ApiController(face_service=face_service, database_repository=db_rep)


async def debug_async():

    api = ApiService(face_service, db_rep)

    novo_user = UserModel.model_validate(admin_user)

    response = await api._count_user(novo_user)
    print(dict(response.data))


async def debug_stream():
    #model = UserModel.model_validate(admin_user)

    async for resposta in api_controller.load_table_user():
        res = resposta.data
        if res is None:
            continue
        
        print(res)

        


def debug():
    novo_user = UserModel.model_validate(admin_user)
    novo_user.set_encoding(_encoding_teste(0.4))
    print(novo_user.model_dump())
    print(novo_user.verificar_senha("admin1234"))


if __name__ == "__main__":

    asyncio.run(debug_stream())
    # debug()
