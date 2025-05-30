""" from controllers.camera_controller import CameraController
from core.errors.camera_exceptions import CameraException
from models.user_model import UserModel
from services.api_service import ApiService
from models.face_model import FaceModel
from core.config.app_config import config
"""
import asyncio
import cv2 

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


async def debug():
   list = [1]
   if not list:
       print("p")
   

if __name__ == "__main__":

    asyncio.run(debug())
