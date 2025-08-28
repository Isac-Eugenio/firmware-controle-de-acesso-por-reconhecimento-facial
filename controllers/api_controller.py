from typing import Any, AsyncGenerator
from core.commands.result import *
from core.utils.api_utils import ApiUtils
from models.device_model import DeviceModel
from models.login_model import LoginModel
from models.perfil_model import PerfilModel
from models.user_model import UserModel
from repository.api_repository import ApiRepository
from services.face_service import FaceService


class ApiController:
    def __init__(self, api_repository: ApiRepository, face_service: FaceService):
        self.api_repository = api_repository
        self.face_service = face_service

    async def register_user_db(
        self, user_data: UserModel, admin_key_access: LoginModel
    ) -> AsyncGenerator[Result[Any, str], None]:
        yield Running("Iniciando registro ...")

        yield Running("Verificando ID do usuario ...")
        is_admin = await self.isAdmin(admin_key_access)

        if is_admin.is_failure:
            if getattr(is_admin, "error", False):
                yield Failure(
                    "Erro ao verificar permissão de admin",
                    details=is_admin.value,
                    error=True,
                )
            else:
                yield Failure("Acesso Negado ao Usuario!", details=is_admin.value)
            return

        yield Running("Usuario Autorizado ...")
        yield Running("iniciando Coleta do rosto ...")

        get_encoding = await self.face_service.get_first_face_encoding_async()
        if get_encoding.is_failure:
            yield Failure(
                "Erro ao coletar o rosto", details=get_encoding.value, error=True
            )
            return

        face_encoding = get_encoding.value
        user_data.set_encoding(face_encoding)

        yield Running("Rosto coletado com sucesso")
        yield Running("Iniciando registro do usuario no banco de dados ...")

        db_result = await self.api_repository.insert_user_table(user_data)
        if db_result.is_failure:
            yield Failure(
                "Erro ao registrar o usuario ...", details=db_result.value, error=True
            )
            return

        yield Success("Usuario registrado com sucesso ...", details=db_result.value)

    async def get_user_table(
        self, admin_data: LoginModel
    ) -> Result[list[PerfilModel], str]:

        auth = await self.isAdmin(admin_data)
        if auth.is_failure:
            if getattr(auth, "error", False):
                return Failure(
                    "Erro interno ao verificar admin",
                    details=auth.value,
                    error=True,
                )
            else:
                return Failure("Acesso Negado ...", details=auth.value)

        result = await self.api_repository.select_user_table()
        if result.is_failure:
            return Failure(
                "Erro ao coletar tabela de usuarios ...",
                details=result.value,
                error=True,
            )

        return Success(result.value, log=result.log)

    async def login(self, login_data: LoginModel) -> Result[PerfilModel, str]:

        result = await self.api_repository.find_user(login_data)

        if result.is_failure:
            if getattr(result, "error", False):
                return Failure(
                    "Erro ao Autorizar o login ...", details=result.value, error=True
                )
            return Failure("Usuario não Autorizado...", log=result.log)

        result_dict = dict(result.value)
        teste = PerfilModel(**result_dict)

        return Success(teste, log="Usuario Autorizado ...")

    async def isAdmin(self, admin_data: LoginModel) -> Result[bool, str]:
        result = await self.api_repository.user_is_admin(admin_data)

        if result.is_failure:
            if getattr(result, "error", False):
                return Failure(
                    "Erro ao verificar se o usuario é admin ...",
                    details=result.value,
                    error=True,
                )
            return Failure("Usuario não autorizado ...", details=result.value)

        if result.value is True:
            return Success(True, log="Usuario autorizado ...")
        return Failure("Usuario não autorizado ...", details=result.value)

    async def find_user(
        self, user_data: dict, admin_data: dict
    ) -> Result[PerfilModel, str]:
        user_data = UserModel(**user_data)
        admin_data = LoginModel(**admin_data)

        auth = await self.isAdmin(admin_data)
        if auth.is_failure:
            if getattr(auth, "error", False):
                return Failure(
                    "Erro interno na verificação de admin",
                    details=auth.value,
                    error=True,
                )
            else:
                return Failure("Acesso Negado ...", details=auth.value)

        result = await self.api_repository.find_user(user_data)
        if result.is_failure:
            return Failure(
                "Erro ao encontrar usuario ...", details=result.value, error=True
            )

        result_value_dict = dict(result.value)
        result_perfil_model = PerfilModel(**result_value_dict)

        return Success(result_perfil_model, log="Usuario encontrado com sucesso ...")

    async def delete_user(
        self, user_data: dict, admin_data: LoginModel
    ) -> Result[None, str]:
        user_data = UserModel(**user_data)
        admin_data = LoginModel(**admin_data)

        auth = await self.isAdmin(admin_data)
        if auth.is_failure:
            if getattr(auth, "error", False):
                return Failure(
                    "Erro interno na verificação de admin",
                    details=auth.value,
                    error=True,
                )
            return Failure("Acesso Negado ...", details=auth.value)

        result = await self.api_repository.delete_user_table(user_data)
        if result.is_failure:
            return Failure(
                "Erro ao deletar usuario ...", details=result.value, error=True
            )

        return Success(None, log="Usuario deletado com sucesso ...")

    async def update_user(
        self, user_data: dict, new_data: dict, admin_data: LoginModel
    ) -> Result[None, str]:
        user_data = UserModel(**user_data)
        admin_data = LoginModel(**admin_data)
        new_data = UserModel(**new_data)

        auth = await self.isAdmin(admin_data)
        if auth.is_failure:
            if getattr(auth, "error", False):
                return Failure(
                    "Erro interno na verificação de admin",
                    details=auth.value,
                    error=True,
                )
            return Failure("Acesso Negado ...", details=auth.value)

        result = await self.api_repository.update_user_table(user_data, new_data)
        if result.is_failure:
            return Failure(
                "Erro ao atualizar usuario ...", details=result.value, error=True
            )

        return Success(None, log="Usuario atualizado com sucesso ...")

    async def open_door(self, device_data: DeviceModel) -> Result[Any, str]:
        return await self.api_repository.open_door(device_data)
