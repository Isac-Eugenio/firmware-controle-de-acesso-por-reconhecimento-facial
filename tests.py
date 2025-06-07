import asyncio
from models.camera_model import CameraModel
from models.face_model import FaceModel
from repository.camera_repository import CameraRepository
from repository.database_repository import DatabaseRepository
from services.api_service import ApiService
from core.config.app_config import config
from services.face_service import FaceService
from core.alias.alias_api import _HOST_CAMERA, _PORT_CAMERA

camera_model = CameraModel(_HOST_CAMERA, _PORT_CAMERA)
camera_repository = CameraRepository(model=camera_model)

face_model = FaceModel()
face_service = FaceService(camera_repository=camera_repository, face_model=face_model)

db_repository = DatabaseRepository()

api = ApiService(face_service, db_repository)


async def debug_async():
    process = await api._load_users()
    print(process)


async def debug_stream():
    pass


def debug():
    pass


if __name__ == "__main__":
    # debug()

    asyncio.run(debug_async())
