import asyncio

from controllers.api_controller import ApiController
from core.commands.async_command import AsyncCommand
from core.commands.stream_command import StreamCommand
from core.config.app_config import CameraConfig
from core.utils.api_utils import ApiUtils
from models.user_model import UserModel

from repository.api_repository import ApiRepository
from repository.camera_repository import CameraRepository
from repository.database_repository import DatabaseRepository

from services.face_service import FaceService



cam_repository = CameraRepository(CameraConfig())
face_service = FaceService(cam_repository)

db_repository = DatabaseRepository()

api_repository = ApiRepository(db_repository)


async def debug_async():
    user_admin_dict = {"id": "00000001"}
    user_admin = UserModel(**user_admin_dict)

    controller = ApiController(api_repository, face_service)

    user_discente_dict = {
        "nome": "João Silva",
        "alias": "joaos",
        "cpf": "123.456.789-00",
        "email": "joao.silva@email.com",
        "matricula": "2025123456",
        "senha": None,
        "icon_path": None,
        "encodings": None,
    }

    user_discente = UserModel(**user_discente_dict)

    stream_command = StreamCommand(
        lambda: controller.register_user_db(user_discente, user_admin)
    )

    async for result in stream_command.execute_stream():
        print(result)


async def teste_async():
    user_login_dict = {"email": "root.debug@gmail.com", "senha": "@Isac1998"}

    user_login = UserModel(**user_login_dict)

    controller = ApiController(api_repository, face_service)

    command = AsyncCommand(lambda: controller.login(user_login_dict))
    result = await command.execute_async()

    #p = AdminModel.from_user(result.value)

    #print(p)

    print(result)

def debug():
    print(len(ApiUtils.generate_128_repeated_floats(2).split(",")))

if __name__ == "__main__":
    asyncio.run(debug_async())
