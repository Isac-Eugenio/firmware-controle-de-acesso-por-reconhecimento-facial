from services.face_service import FaceService
from services.login_service import LoginService
from services.api_service import ApiService
from core.utils.FaceUtils import FaceUtils
from core.Camera import Camera
from core.config.config import config
from db.Database import Database
import asyncio

db = Database()
face_service = FaceService()
api = ApiService()
_camera = Camera(config["hosts"]["camera"], config["ports"]["camera"])
_frame = _camera.get_frame(config["details"]["camera"]["resolution"], 
                                config["details"]["camera"]["format"])

async def debug():
    # DEBUG DO BANCO DE DADOS
    # Para testar o banco de dados, descomente o código abaixo e execute o arquivo
    user = {
            "cpf": "000.000.000-01",
            "alias":"Isac",
            "matricula": "0000000",
            "email":"discente@gmail.com",
            "nome": "teste1",
            "auth": "discente",
            "encodings": "1,0,0,0,0,0"
        } 
    admin = {
        "id" : '80679543'
    }
    data = {
        "admin_data":admin,
        "user_data":user
    }
    
    try:
        get = await api.insert_user_api(form=data)
        print(get)

    except Exception as e:
        print(e)

  
    

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

    asyncio.run(debug())
