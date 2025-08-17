import asyncio
from core.commands.async_command import AsyncCommand
from core.commands.result import Result, Running, Success, Failure
from core.config.app_config import CameraConfig
from core.utils.api_utils import ApiUtils
from models.baseuser_model import BaseUserModel
from models.camera_model import CameraModel
from models.face_model import FaceModel
from models.query_model import QueryModel
from models.user_model import UserModel
from repository.camera_repository import CameraRepository
from repository.database_repository import DatabaseRepository
from services.face_service import FaceService
from services.ping_service import PingService


cam_repository = CameraRepository(CameraConfig())
face_service = FaceService(cam_repository)


async def debug_async():
    query = QueryModel(table="usuarios")
    db = DatabaseRepository()

    face_model = face_service.create_face_model()

    if face_model.is_failure:
        print(face_model.value)

    encoding = face_model.value._encoding_string(face_model.value.encodings)

    user_model = UserModel(
        id=ApiUtils._generate_id(),
        nome="elias",
        alias="eu",
        cpf="030.000.000-00",
        email="eu@gmail.com",
        matricula=None,
        senha=None,
        icon_path=None,
        permission_level="discente",
    )

    user_model.set_encoding(encoding.value)

    query.values = user_model.to_map().value

    res  = await db.insert(query)
    
    print(res)
    if encoding.is_failure:
        print(encoding.value)
    


def debug():
   
    p = face_service.create_face_model()
    print(p)
 
       
if __name__ == "__main__":
   asyncio.run(debug_async())