from models.user_model import UserModel
from services.login_service import LoginService
from services.api_service import ApiService
from models.face_model import FaceUtils
from core.Camera import Camera
from core.config.config import config
from services.database_service import DatabaseService
import asyncio

db = DatabaseService()
api = ApiService()

_camera = Camera(config["hosts"]["camera"], config["ports"]["camera"])
_frame = _camera.get_frame(config["details"]["camera"]["resolution"], 
                                config["details"]["camera"]["format"])


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
}

async def debug_stream():
    """ try:
        async for step in face_service._validate_user(
            columns=["nome", "id"],
            encoding_column="encodings",
            table="usuarios",
            trust=60
        ):
              print(step['message'])
            
    except Exception as e:
        print(f"data: Erro ao processar: {str(e)}\n\n") """
    
    try:
        async for step in api._insert_user(
            data=data,
            encoding_column="encodings",
            table="usuarios"):
              print(step['message'])
            
    except Exception as e:
        print(f"data: Erro ao processar: {str(e)}\n\n") 


async def debug():
   result = api._extract_valid_face_encoding()
   encoding = ",".join(str(x) for x in result["encoding"])
   print(encoding)
""" 
     # DEBUG DA CÂMERA
    # Para testar a câmera, descomente o código abaixo e execute o arquivo

camera_info = {
    "host": config["hosts"]["camera"],
    "port": config["ports"]["camera"],
    "resolution": config["details"]["camera"]["resolution"],
    "format": config["details"]["camera"]["format"]
}

camera = Camera(camera_info["host"], camera_info["port"])
frame = camera.get_frame(camera_info["resolution"], camera_info["format"])
 """
""" 
DEBUG DA FACEUTILS
    # Para testar o FaceUtils, descomente o código abaixo e execute o arquivo
face_utils = FaceUtils(frame)
print(face_utils.encodings()) """


if __name__ == "__main__":

    asyncio.run(debug)
