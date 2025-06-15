from core.errors.api_exception import ApiDatabaseError
from models.face_model import FaceModel
from models.login_model import LoginModel
from models.response_model import ResponseModel
from repository.database_repository import DatabaseRepository
from models.query_model import QueryModel
from services.face_service import FaceService
from core.config.app_config import *
from models.user_model import UserModel
import numpy as np


class ApiService:
    def __init__(
        self, face_service: FaceService, database_repository: DatabaseRepository
    ):
        self.face_service = face_service
        self.db_repository = database_repository
        self._model = QueryModel(table=DatabaseTables.perfis)
        self.perfil_columns = PerfisColumns()

    async def _load_users_with_encodings(self):
        try:
            response = []
            query = QueryModel(table=DatabaseTables.perfis)
            query.columns = self.perfil_columns.full_columns

            result = await self.db_repository.select(query)

            if result.error:
                return result

            for row in result.data:
                row_dict = dict(row)

                # Extrai e define encoding separadamente
                encoding_str = row_dict.pop(self.perfil_columns.encoding, "")
                model = UserModel()
                model.set_encoding(encoding_str)

                # Valida os demais dados
                model = UserModel.model_validate(row_dict)

                response.append(model)

            return ResponseModel(
                log="Perfis carregados com sucesso",
                status=True,
                error=False,
                data=response,
            )

        except Exception as e:
            return ResponseModel(
                log="Erro ao carregar perfis",
                error=True,
                status=True,
                details=str(e),
                data=None,
            )

    async def _load_users(self):
        try:
            response = []
            query = QueryModel(table=DatabaseTables.perfis)

            # Define apenas as colunas que não envolvem encoding
            query.columns = (
                self.perfil_columns.private
            )  # ou .public, dependendo da lógica

            result = await self.db_repository.select(query)

            if result.error:
                return result

            for row in result.data:
                row_dict = dict(row)

                # Valida e instancia o modelo sem encoding
                model = UserModel.model_validate(row_dict)

                response.append(model)

            return ResponseModel(
                log="Perfis carregados com sucesso (sem encoding)",
                status=True,
                error=False,
                data=response,
            )

        except Exception as e:
            return ResponseModel(
                log="Erro ao carregar perfis (sem encoding)",
                error=True,
                status=True,
                details=str(e),
                data=None,
            )

    """ 
    TODO: Manutenção
    async def _insert_user(self, user_model: UserModel, face_model: FaceModel):
        try:
            user_dict = user_model.to_dict()
            encoding_str = FaceModel._encoding_array(face_model.encoding)

            user_dict[_ENCODING_COLUMN] = encoding_str

            insert_model = QueryModel(
                table=_NAME_TABLE_PERFIS,
                columns=list(user_dict.keys()),
                values=list(user_dict.values())
            )

            result = await self.db_repository.insert(insert_model)

            if result.error:
                raise ApiDatabaseError("Erro ao inserir usuário")

            return ResponseModel(
                log="Usuário inserido com sucesso",
                status=True,
                error=False
            )

        except Exception as e:
            return ResponseModel(
                log="Erro ao inserir usuário",
                error=True,
                status=True,
                details=str(e)
            ) """
