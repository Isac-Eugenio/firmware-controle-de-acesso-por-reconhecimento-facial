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
    """  data = {
            "cpf": "111.111.111-00",
            "alias":"Isac",
            "matricula": "0000000",
            "email":"discente@gmail.com",
            "nome": "teste1",
            "auth": "discente",
            ""
        } """
    
    data = {"admin_data": {"id": "0000", "auth": "admin"}}
    try:
        get = await api.insert_user_api(form=data)
        """ async for steps in face_service.insert_user(data=data, encoding_column="encodings", table="usuarios"):
            if not steps["final"]:
                print("Processando:", steps["message"])
            else:
                print("Finalizado:", steps["message"])  """
        
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
