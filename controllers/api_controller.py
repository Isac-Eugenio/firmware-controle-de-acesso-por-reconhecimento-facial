from models.response_model import ResponseModel
from models.user_model import UserModel
from repository.database_repository import DatabaseRepository
from services.api_service import ApiService
from services.face_service import FaceService


class ApiController:
    def __init__(
        self, face_service: FaceService, database_repository: DatabaseRepository
    ):
        self.api_service = ApiService(face_service, database_repository)

    async def login(self, user_model: UserModel):
        try:
            yield ResponseModel(status=False, error=False, log="Verificando Login")

            task = await self.api_service._count_user(user_model)
            response_dict = dict(task.data)

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="Erro no Login",
                    details=task.details,
                )

                return

            if response_dict.get("total", 0) > 0:
                yield ResponseModel(
                    status=True,
                    error=False,
                    log="Login bem-sucedido",
                    data=response_dict,
                )
            else:
                yield ResponseModel(
                    status=True,
                    error=False,
                    log="Email ou senha incorretos !",
                    data=response_dict,
                )

            return
        except (Exception, ValueError) as e:
            yield ResponseModel(
                status=False,
                error=True,
                log="Erro ao processar login",
                details=str(e),
            )

            return
