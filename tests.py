from services.login_service import LoginService
from services.api_service import ApiService
from core.FaceUtils import FaceUtils
from core.Camera import Camera
from core.config import config
from db.Database import Database
import asyncio

db = Database()

async def debug():
    # DEBUG DO BANCO DE DADOS
    # Para testar o banco de dados, descomente o código abaixo e execute o arquivo
    list_result = []
    service = ApiService()
    result = await service.get_table(columns=["nome", "email", "auth"],table="usuarios")
    for i in result['result']:
        list_result.append(dict(i))
    
    print(list_result)
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
