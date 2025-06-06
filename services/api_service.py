from core.errors.api_exception import ApiDatabaseError
from models.face_model import FaceModel
from models.response_model import ResponseModel
from repository.database_repository import DatabaseRepository
from models.query_model import QueryModel
from services.face_service import FaceService
from core.config.app_config import config
from models.user_model import UserModel
import numpy as np


_ENCODING_COLUMN = _ENCODING_COLUMN = config["details"]["database"]["tables"]["perfis"][
    "encoding_column"
]
_NAME_TABLE_PERFIS = config["details"]["database"]["tables"]["perfis"]["name"]
_COLUMNS_TABLE_PERFIS = config["details"]["database"]["tables"]["perfis"]["columns"]


class ApiService:
    def __init__(
        self, face_service: FaceService, database_repository: DatabaseRepository
    ):
        self.face_service = face_service
        self.db_repository = database_repository
        self._model = QueryModel(table=_NAME_TABLE_PERFIS)

    async def _load_users_with_encodings(self):
        try:
            response = []

            query = QueryModel(table=_NAME_TABLE_PERFIS)
            query.columns = _COLUMNS_TABLE_PERFIS.copy()
            query.columns.append(_ENCODING_COLUMN)

            result = await self.db_repository.select(query)

            if result.error:
                return result

            for row in result.data:
                row_dict = dict(row)
                encoding_str = row_dict.pop(_ENCODING_COLUMN, "")

                user_model = UserModel.from_dict(row_dict)

                if encoding_str:
                    encoding_array = FaceModel._encoding_array(encoding_str)
                    user_model._face_model = FaceModel(encoding=encoding_array)

                response.append(user_model)

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

            query = QueryModel(table=_NAME_TABLE_PERFIS)
            query.columns = _COLUMNS_TABLE_PERFIS.copy()

            result = await self.db_repository.select(query)

            if result.error:
                return result

            for row in result.data:
                row_dict = dict(row)

                user_model = UserModel.from_dict(row_dict)

                response.append(user_model)

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
    