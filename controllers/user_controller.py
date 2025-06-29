from core.errors.database_exception import DatabaseException
from core.errors.face_exceptions import FaceRecognitionException
from models.login_model import LoginModel
from models.response_model import ResponseModel
from models.user_model import UserModel
from repository.database_repository import DatabaseRepository
from services.user_service import UserService
from services.face_service import FaceService


class UserController:
    def __init__(
        self, face_service: FaceService, database_repository: DatabaseRepository
    ):
        self.user_service = UserService(face_service, database_repository)
        self.face_service = face_service

    async def login(self, login_model: LoginModel):
        try:

            yield ResponseModel(status=False, error=False, log="Verificando Login")

            task = await self.user_service._login_user(login_model)

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="Erro no Login",
                    details=task.details,
                )

            yield task
            return

        except (Exception, ValueError) as e:
            yield ResponseModel(
                status=False,
                error=True,
                log="Erro ao processar login",
                details=str(e),
            )

            return

    async def register(self, user_model: UserModel, login_model: LoginModel):
        try:
            yield ResponseModel(status=False, error=False, log="Iniciando Registro")

            yield ResponseModel(status=False, error=False, log="Verificando ID")

            task = await self.user_service._verify_user_with_id(login_model)
            if task.error:
                yield  ResponseModel(status=True, error=True, log="Erro ao verificar ID", details=task.details)
                return 
            
            if task.data is None or not task.data:
                yield  ResponseModel(status=True, error=True, log="ID não Autorizado", details=task.details)
                return 
            
            yield ResponseModel(status=False, error=False, log="ID Autorizado")

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

            task = await self.user_service._insert_user(user_model)

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

    async def load_data(self):
        try:
            yield ResponseModel(status=False, error=False, log="Carregando Tabela")
            task = await self.user_service._load_users()

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

    async def update(self, user_model: UserModel, new_model: UserModel):
        try:
            yield ResponseModel(status=False, error=False, log="Atualizando Usuario")

            yield ResponseModel(status=False, error=False, log="Atualizando Usuario")
            task = await self.user_service._update_user(user_model, new_model)

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="Error ao Atualizar o Usuario",
                    details=task.details,
                )
                return

            yield ResponseModel(
                status=True, error=False, log="Usuario Atualizado com sucesso"
            )
            return

        except (Exception, ValueError) as e:
            yield ResponseModel(
                status=True,
                error=False,
                log="Erro ao Atualizar o Usuario",
                details=str(e),
            )
