
import asyncio
import cv2
import numpy as np

from models.camera_model import CameraModel
from models.face_model import FaceModel 

from core.config.app_config import config
from repository.camera_repository import CameraRepository

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


async def debug_async():
   pass

_HOST_CAMERA = config["hosts"]["camera"]
_PORT_CAMERA = config["ports"]["camera"]
_CONFIG_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CONFIG_CAMERA_FORMAT = config["details"]["camera"]["format"]


modelo_teste = CameraModel(_HOST_CAMERA, _PORT_CAMERA)
repository_teste = CameraRepository(model=modelo_teste)

def debug():
   process =repository_teste.get_frame(_CONFIG_CAMERA_RESOLUTION, _CONFIG_CAMERA_FORMAT)
   print(process)

if __name__ == "__main__":
   debug()

