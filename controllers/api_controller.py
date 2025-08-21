from core.commands.result import *
from core.utils.api_utils import ApiUtils
from models.login_model import LoginModel
from models.perfil_model import PerfilModel
from models.user_model import UserModel
from repository.api_repository import ApiRepository
from services.face_service import FaceService


class ApiController:
    def __init__(self, api_repository: ApiRepository, face_service: FaceService):
        self.api_repository = api_repository
        self.face_service = face_service

    async def register_user_db(self, user_data: UserModel, admin_key_access: UserModel):
        yield Running("Iniciando registro ...")

        admin_key_access_dict = admin_key_access.model_dump(
            exclude_none=True, exclude_unset=True
        )
        yield Running("Verificando ID do usuario ...")

        is_admin = await self.api_repository.user_is_admin(user_data=admin_key_access)
        if is_admin.is_failure:
            yield Failure("Acesso Negado ao Usuario!", details=is_admin.value)
            return

        if is_admin.is_success:
            if is_admin.value:
                yield Running("Usuario Autorizado ...")

            else:
                yield Failure("Acesso Negado ao Usuario!", details=is_admin.value)
                return

        yield Running("iniciando Coleta do rosto ...")

        get_encoding = self.face_service.get_first_face_encoding()

        if get_encoding.is_failure:
            yield Failure("Erro ao coletar o rosto", details=get_encoding.value)
            return

        face_encoding = get_encoding.value

        user_data.set_encoding(face_encoding)

        yield Running("Rosto coletado com sucesso")

        yield Running("Iniciando registro do usuario no banco de dados ...")

        db_result = await self.api_repository.insert_user_table(user_data)
        if db_result.is_failure:
            yield Failure("erro ao registrar o usuario ...", details=db_result.value)
            return

        yield Success("Usuario registrado com sucesso ...", details=db_result.value)

    async def login(self, login_data: dict) -> Result[PerfilModel, str]:

        login_data = LoginModel(**login_data)

        result = await self.api_repository.find_user(login_data)

        if result.is_failure:
            if result.log is None:
                return Failure("Erro ao Autorizar o login ...", details=result.value)

            return Failure("Usuario não Autorizado...", log=result.log)

        result_dict = dict(result.value)

        teste = PerfilModel(**result_dict)

        return Success(teste, log="Usuario Autorizado ...")
