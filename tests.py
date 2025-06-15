import asyncio
from pydantic import ValidationError
from core.config.app_config import CameraConfig as Camera, DatabaseConfig, DatabaseTables, PerfisColumns
from models.baseuser_model import BaseUserModel, PermissionLevel
from models.face_model import FaceModel
from models.login_model import LoginModel
from models.camera_model import CameraModel
from models.query_model import QueryModel
from models.response_model import ResponseModel
from models.user_model import UserModel
from repository.camera_repository import CameraRepository
from repository.database_repository import DatabaseRepository, DATABASE_URL
from services.api_service import ApiService
from services.face_service import FaceService



def _encoding_teste():
    zeros_float_str = ",".join(["0.1"] * 128)
    return zeros_float_str

async def debug_async():
    camera_rep = CameraRepository(Camera)
    db_rep = DatabaseRepository()
    face_model = FaceModel()
    face_service = FaceService(camera_rep, face_model)
    api = ApiService(face_service, db_rep)
    
    response = await api._load_users()
    data = response.data
    for i in data:
        print(i.model_dump())


async def debug_stream():
    pass


def debug():
    print(PerfisColumns().full_columns)


if __name__ == "__main__":

    asyncio.run(debug_async())
