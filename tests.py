import face_recognition as fr
import asyncio
import cv2
import numpy as np

from core.utils.api_utils import ApiUtils
from models.dataclass.response_model import ResponseModel
from models.dataclass.query_model import QueryModel
from models.user_model import UserModel
from repository.database_repository import DatabaseRepository
from services.face_service import FaceService
from models.camera_model import CameraModel
from models.face_model import FaceModel

from core.config.app_config import config
from repository.camera_repository import CameraRepository
from services.face_service import FaceService

""" 
api = ApiService()

_modelo = UserModel()

senha = _modelo.set_senha("@Isac1998")

_modelo.nome = "Isac"
data = {
    "admin_data": {
        "id": '00000001',
        "email": "root.debug@gmail.com"
    },
    "user_data": {
        "cpf": "010.100.000-01",
        "alias": "Isac",
        "matricula": "0000000",
        "email": "discente@gmail.com",
        "nome": "teste1",
        "auth": "discente",
    }
} """


async def debug_stream():
    pass
    """ try:
        async for step in api._insert_user(
            data=data,
            encoding_column="encodings",
            table="usuarios"):
              print(step['message'])
            
    except Exception as e:
        print(f"data: Erro ao processar: {str(e)}\n\n")  """


user_model = UserModel()
database_repository = DatabaseRepository()

query_model = QueryModel(table="usuarios")

utils = ApiUtils()



async def debug_async():

    await database_repository._ensure_connected()
    process = await database_repository.count(query_model)

    await database_repository._disconnect()

    print(dict(process.data))


_HOST_CAMERA = config["hosts"]["camera"]
_PORT_CAMERA = config["ports"]["camera"]
_CONFIG_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CONFIG_CAMERA_FORMAT = config["details"]["camera"]["format"]


camera_model = CameraModel(_HOST_CAMERA, _PORT_CAMERA)
camera_repository = CameraRepository(model=camera_model)

face_model = FaceModel()
face_controller = FaceService(
    camera_repository=camera_repository, face_model=face_model
)


def debug():
   
    process = query_model.select()
    print(query_model.query)


if __name__ == "__main__":
    #debug()

   asyncio.run(debug_async())
