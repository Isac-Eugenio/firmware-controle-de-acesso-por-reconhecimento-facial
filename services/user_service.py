from core.errors.api_exception import ApiDatabaseError
from core.utils.api_utils import ApiUtils
from models.face_model import FaceModel
from models.login_model import LoginModel
from models.response_model import ResponseModel
from repository.database_repository import DatabaseRepository
from models.query_model import QueryModel
from services.face_service import FaceService
from core.config.app_config import *
from models.user_model import UserModel
import numpy as np


class UserService:
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
                log="Erro interno no Servidor",
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
                log="Erro interno no Servidor",
                error=True,
                status=True,
                details=str(e),
                data=None,
            )

    async def _count_user(self, user_model: UserModel):
        try:
            model_dict = user_model.model_dump()
            model_dict = ApiUtils._limpar_dict(model_dict)

            query = QueryModel(
                table=DatabaseTables.perfis,
                values=model_dict,
            )

            result = await self.db_repository.count(query)

            if result.error:
                return ResponseModel(
                    log="Erro ao contar usuários",
                    error=True,
                    status=True,
                    details=result.details,
                )

            return ResponseModel(
                log="Contagem de usuários realizada com sucesso",
                status=True,
                error=False,
                data=result.data,
            )

        except Exception as e:
            return ResponseModel(
                log="Erro interno no Servidor", error=True, status=True, details=str(e)
            )

    async def _insert_user(self, user_model: UserModel):
        try:
            model_dict = user_model.model_dump()
            query = QueryModel(
                table=DatabaseTables.perfis,
                values=model_dict,
            )

            result = await self.db_repository.insert(query)
            if result.error:
                return ResponseModel(
                    log="Erro ao inserir usuário",
                    error=True,
                    status=True,
                    details=result.details,
                )

            return ResponseModel(
                log="Usuário inserido com sucesso", status=True, error=False
            )

        except Exception as e:
            return ResponseModel(
                log="Erro interno no Servidor", error=True, status=True, details=str(e)
            )

    async def _update_user(self, user_model: UserModel, new_model: UserModel):
        try:

            model_dict = ApiUtils._limpar_dict(user_model.model_dump())
            new_model_dict = ApiUtils.limpar_dict(new_model.model_dump())

            query = QueryModel(table=DatabaseTables.perfis, values=model_dict)
            new_query = QueryModel(table=DatabaseTables.perfis, values=new_model_dict)

            result = await self.db_repository.update(query, new_query)

            if result.error:
                return ResponseModel(
                    log="Erro ao atualizar usuário",
                    error=True,
                    status=True,
                    details=result.details,
                )

            return ResponseModel(
                log="Usuário atualizado com sucesso", status=True, error=False
            )

        except Exception as e:
            return ResponseModel(
                log="Erro interno no Servidor", error=True, status=True, details=str(e)
            )

    async def _delete_user(self, user_model: UserModel):
        try:
            model_dict = user_model.model_dump()
            model_dict = ApiUtils._limpar_dict(model_dict)

            query = QueryModel(
                table=DatabaseTables.perfis,
                values=model_dict,
            )

            result = await self.db_repository.delete(query)

            if result.error:
                return ResponseModel(
                    log="Erro ao deletar usuário",
                    error=True,
                    status=True,
                    details=result.details,
                )

            return ResponseModel(
                log="Usuário deletado com sucesso", status=True, error=False
            )

        except Exception as e:
            return ResponseModel(
                log="Erro interno no Servidor", error=True, status=True, details=str(e)
            )

    async def _login_user(self, login_model: LoginModel):
        try:
            model_dict = login_model.model_dump()
            columns = list(model_dict.keys())
            columns_null = ApiUtils._limpar_dict(model_dict).keys()
            conditions = [f"{key} = :{key}" for key in columns_null]
            where_clause = " AND ".join(conditions)

            query = QueryModel(
                table=DatabaseTables.perfis,
                condition=where_clause,
                columns=columns,
                values=ApiUtils._limpar_dict(model_dict),
            )

            task = await self.db_repository.select_one(query)
            if task.error:
                return ResponseModel(
                    status=True,
                    error=False,
                    log="Erro ao verificar o Usuario",
                    data=None,
                    details=task.details,
                )

            if task.data is None:
                return ResponseModel(
                    status=True,
                    error=True,
                    log="Email ou senha incorretos!",
                    data=None,
                )

            return ResponseModel(
                status=True,
                error=False,
                log="Login bem-sucedido",
                data=task.data,
            )

        except Exception as e:
            return ResponseModel(
                status=True,
                error=True,
                log="Erro interno no Servidor",
                data=None,
                details=str(e),
            )

    async def _verify_user_with_id(self, login_model: LoginModel) -> ResponseModel:
        try:
            if not login_model.id:
                return ResponseModel(
                    status=False, error=True, log="ID ausente", data=None
                )

            task = await self._count_user(login_model)

            if task.error:
                return ResponseModel(
                    status=False, error=True, log="Erro ao Analisar ID", data=task.data
                )

            total = dict(task.data).get("total", 0)
            return ResponseModel(
                status=True,
                error=False,
                log="Usuário verificado" if total > 0 else "Usuário não encontrado",
                data=total > 0,
            )

        except Exception as e:
            return ResponseModel(
                status=False, error=True, log=f"Erro interno: {str(e)}", data=None
            )
