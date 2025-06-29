from typing import AsyncGenerator
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
            yield ResponseModel(status=False, error=False, log="Iniciando Registro")

            # Etapa 1: Verificando ID
            task = await self.user_service._verify_user_with_id(login_model)
            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="Erro ao verificar ID",
                    details=str(task.details),
                )
                return

            if task.data is None or not task.data:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="ID não Autorizado",
                    details=str(task.details),
                )
                return

            yield ResponseModel(status=False, error=False, log="ID Autorizado")

            # Etapa 2: Registrando usuário com rosto
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
                    details=str(task.details),
                )
                return

            yield ResponseModel(
                status=True, error=False, log="Usuário registrado com sucesso"
            )

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

    async def load_data(
        self, login_model: LoginModel
    ) -> AsyncGenerator[ResponseModel, None]:
        try:
            yield ResponseModel(
                status=False, error=False, log="🔐 Verificando permissão de acesso"
            )

            # Verifica o ID do usuário
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
            yield ResponseModel(
                status=False, error=False, log="📥 Carregando tabela de usuários"
            )

            # Carrega os dados
            task = await self.user_service._load_users()

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="❌ Erro ao carregar a tabela",
                    details=str(task.details),
                )
                return

            yield ResponseModel(
                status=True,
                error=False,
                log="✅ Tabela carregada com sucesso",
                data=task.data,
            )

        except Exception as e:
            yield ResponseModel(
                status=True,
                error=True,
                log="❌ Erro inesperado ao carregar tabela",
                details=str(e),
            )

    async def update(
        self, login_model: LoginModel, user_model: UserModel, new_model: UserModel
    ) -> AsyncGenerator[ResponseModel, None]:
        try:
            yield ResponseModel(
                status=False, error=False, log="🔐 Verificando permissão de atualização"
            )

            # Verifica o ID do usuário atual (quem está tentando atualizar)
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
            yield ResponseModel(status=False, error=False, log="🔄 Atualizando usuário")

            # Executa atualização
            task = await self.user_service._update_user(user_model, new_model)

            if task.error:
                yield ResponseModel(
                    status=True,
                    error=True,
                    log="❌ Erro ao atualizar o usuário",
                    details=str(task.details),
                )
                return

            yield ResponseModel(
                status=True, error=False, log="✅ Usuário atualizado com sucesso"
            )

        except Exception as e:
            yield ResponseModel(
                status=True,
                error=True,
                log="❌ Erro inesperado ao atualizar usuário",
                details=str(e),
            )
