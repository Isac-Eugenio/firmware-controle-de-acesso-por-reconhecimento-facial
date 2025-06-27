from core.errors.database_exception import DatabaseException
from core.errors.face_exceptions import FaceRecognitionException
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
        self.face_service = face_service

    async def login(self, user_model: UserModel):
        try:
            user_model.permission_level = "administrador"

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
                    data=True,
                )
            else:
                yield ResponseModel(
                    status=True,
                    error=False,
                    log="Email ou senha incorretos !",
                    data=False,
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

    async def register_user(self, user_model: UserModel):
        try:
            yield ResponseModel(status=False, error=False, log="Iniciando Registro")

            yield ResponseModel(status=False, error=False, log="Coletando Rosto")

            self.face_service.create_face_model()

            encoding = self.face_service.face_model.encodings

            user_model.set_encoding(encoding)

            yield ResponseModel(
                status=False, error=False, log="Rosto Coletado com Sucesso"
            )

            yield ResponseModel(
                status=False, error=False, log="Adicionando novo usuario"
            )

            task = await self.api_service._insert_user(user_model)

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="Erro ao registrar usuário",
                    details=task.details,
                )
                return

            yield ResponseModel(
                status=True, error=False, log="Usuário registrado com sucesso"
            )
            return

        except FaceRecognitionException as e:
            yield ResponseModel(
                status=True,
                error=True,
                log="Erro ao Coletar o Rosto",
                details=str(e),
            )

        except (Exception, ValueError) as e:
            yield ResponseModel(
                status=True,
                error=True,
                log="Erro ao processar registro",
                details=str(e),
            )
            return

    async def load_table_user(self):
        try:
            yield ResponseModel(status=False, error=False, log="Carregando Tabela")
            task = await self.api_service._load_users()

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="Erro ao  Carregar tabela",
                    details=task.details,
                )
                return

            yield ResponseModel(
                status=True,
                error=False,
                log="Tabela Carregada com Sucesso",
                data=task.data,
            )
            return

        except (Exception, ValueError) as e:
            yield ResponseModel(
                status=True,
                error=True,
                log="Erro ao Carregar Tabela",
                details=str(e),
            )
            return
