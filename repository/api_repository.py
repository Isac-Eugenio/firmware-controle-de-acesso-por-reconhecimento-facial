from typing import List, Union

from numpy import record
from core.commands.result import Failure, Result, Success
from core.config.app_config import DatabaseTables
from models.login_model import LoginModel
from models.perfil_model import PerfilModel
from models.query_model import QueryModel
from models.user_model import UserModel, PermissionEnum
from repository.database_repository import DatabaseRepository


class ApiRepository:
    def __init__(self, db_repository: DatabaseRepository):
        self.db = db_repository

    async def select_user_table(self) -> Result[List[PerfilModel], str]:
        query = QueryModel(table=DatabaseTables.perfis)

        result = await self.db.select(query)

        if result.is_failure:
            return Failure("Erro ao coletar tabela de usuários", details=result.value)

        filtered_result = []
        for record in result.value:
            dict_t = dict(record)
            perfil = PerfilModel(**dict_t)
            filtered_result.append(perfil)

        return Success(filtered_result, log="Tabela de usuários coletada com sucesso")

    async def insert_user_table(self, user_data: UserModel) -> Result[str, str]:

        user_data_dict = user_data.model_dump()

        query = QueryModel(table=DatabaseTables.perfis, values=user_data_dict)

        result = await self.db.insert(query)

        if result.is_failure:
            return Failure("Erro ao inserir usuário", details=result.value)

        return Success(result.value, log="Usuário inserido com sucesso")

    async def update_user_table(
        self, user_data: UserModel, new_user_data: UserModel
    ) -> Result[str, str]:
        user_data_dict = user_data.model_dump(exclude_none=True, exclude_unset=True)
        new_user_data_dict = new_user_data.model_dump(
            exclude_none=True, exclude_unset=True
        )

        query = QueryModel(table=DatabaseTables.perfis, values=user_data_dict)
        new_query = QueryModel(table=DatabaseTables.perfis, values=new_user_data_dict)

        result = await self.db.update(query=query, new_query=new_query)

        if result.is_failure:
            return Failure("Erro ao atualizar usuário", details=result.value)

        if result.value == 0:
            return Failure("Nenhum foi usuário atualizado", details=result.value)

        if result.value >= 2:
            return Failure("Mais de um usuário foi atualizado", details=result.value)

        return Success(result.value, log="Usuário atualizado com sucesso")

    async def delete_user_table(self, user_data: UserModel) -> Result[str, str]:
        query = QueryModel(
            table=DatabaseTables.perfis, values=user_data.model_dump(exclude_unset=True)
        )

        result = await self.db.delete(query)

        if result.is_failure:
            return Failure("Erro ao deletar usuário", details=result.value)

        return Success(result.value, log="Usuário deletado com sucesso")

    async def user_is_admin(self, user_data: UserModel) -> Result[bool, str]:

        user_data.permission_level = PermissionEnum.ADMINISTRADOR

        user_data_dict = user_data.model_dump(exclude_none=True, exclude_unset=True)

        query = QueryModel(table=DatabaseTables.perfis, values=user_data_dict)

        result = await self.db.count(query)

        if result.is_failure:
            return Failure(
                "Erro ao verificar permissões do usuário", details=result.value
            )

        dict_count_result = dict(result.value)

        if dict_count_result.get("total") > 0:
            return Success(True, log="Usuário é um administrador")

        return Success(
            False,
            log="Usuario não é um administrador",
        )

    async def find_user(
        self, user_data: Union[PerfilModel, UserModel, LoginModel]
    ) -> Result[PerfilModel, str]:
        user_data_dict = user_data.model_dump(exclude_none=True, exclude_unset=True)

        if not user_data_dict:
            return Failure("Erro ao ler dados do request")

        query = QueryModel(table=DatabaseTables.perfis, values=user_data_dict)

        result = await self.db.select_one(query)

        if result.is_failure:
            return Failure("Erro ao encontrar usuário", details=result.value)

        if result.value is None:
            return Failure("Usuário não encontrado", log=result.log)
        return Success(_value=result.value, log="Usuário encontrado com sucesso")
