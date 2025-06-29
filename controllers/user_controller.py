from typing import AsyncGenerator
from core.errors.database_exception import DatabaseException
from core.errors.face_exceptions import FaceRecognitionException
from core.utils.api_utils import ApiUtils
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
                    details=str(task.details),
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

    async def register(
        self,
        user_model: UserModel,
        login_model: LoginModel,
    ) -> AsyncGenerator[ResponseModel, None]:
        try:
            yield ResponseModel(status=False, error=False, log="🔐 Verificando permissão de acesso")

            # Etapa 1: Verificando ID
            task = await self.user_service._verify_user_with_id(login_model)
            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="❌ Erro ao verificar ID",
                    details=str(task.details),
                )
                return

            if task.data is None or not task.data:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="❌ ID não autorizado",
                    details=str(task.details),
                )
                return

            yield ResponseModel(status=False, error=False, log="✅ ID autorizado")

            # Etapa 2: Registrando usuário com rosto
            yield ResponseModel(
                status=False, error=False, log="📸 Coletando rosto do usuário"
            )
            self.face_service.create_face_model()
            encoding = self.face_service.face_model.encodings
            user_model.set_encoding(encoding)

            yield ResponseModel(
                status=False, error=False, log="😀 Rosto coletado com sucesso"
            )
            yield ResponseModel(
                status=False, error=False, log="➕ Adicionando novo usuário"
            )

            task = await self.user_service._insert_user(user_model)

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="❌ Erro ao registrar usuário",
                    details=str(task.details),
                )
                return

            yield ResponseModel(
                status=True, error=False, log="✅ Usuário registrado com sucesso"
            )

        except FaceRecognitionException as e:
            yield ResponseModel(
                status=True,
                error=True,
                log="❌ Erro ao coletar o rosto",
                details=str(e),
            )

        except (Exception, ValueError) as e:
            yield ResponseModel(
                status=True,
                error=True,
                log="❌ Erro ao processar registro",
                details=str(e),
            )

    async def delete(
        self, login_model: LoginModel, user_model: UserModel
    ) -> AsyncGenerator[ResponseModel, None]:
        try:
            yield ResponseModel(
                status=False, error=False, log="🔐 Verificando permissão de acesso"
            )

            # Verifica o ID do usuário atual (quem está tentando deletar)
            task = await self.user_service._verify_user_with_id(login_model)

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="❌ Erro ao verificar ID",
                    details=str(task.details),
                )
                return

            if task.data is None or not task.data:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="❌ ID não autorizado",
                    details="ID inválido ou sem permissão",
                )
                return

            yield ResponseModel(status=False, error=False, log="✅ Acesso autorizado")
            yield ResponseModel(status=False, error=False, log="🗑️ Deletando usuário")

            yield ResponseModel(status=False, error=False, log="🔐 Autorizando exclusão")

            task = await self.user_service._count_user(user_model)

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="❌ Erro ao deletar o usuário",
                    details=str(task.details),
                )
                return

            data = dict(task.data)
            auth = (data.get("total", 0) > 0)
            if auth:
                yield ResponseModel(status=False, error=False, log="✅ Exclusão autorizada")
                # Executa exclusão
                task = await self.user_service._delete_user(user_model)

                if task.error:
                    yield ResponseModel(
                        status=True,
                        error=True,
                        log="❌ Erro ao deletar o usuário",
                        details=str(task.details),
                    )
                    return

            else:
                yield ResponseModel(status=True, error=False, log="❌ Exclusão não autorizada")
                return

            yield ResponseModel(
                status=True, error=False, log="✅ Usuário deletado com sucesso"
            )

        except Exception as e:
            yield ResponseModel(
                status=True,
                error=True,
                log="❌ Erro inesperado ao deletar usuário",
                details=str(e),
            )
