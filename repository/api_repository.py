from typing import List, Union

from numpy import record
from core.commands.result import Failure, Result, Success
from core.config.app_config import DatabaseTables
from models.query_model import QueryModel
from models.user_model import UserModel, PermissionEnum
from repository.database_repository import DatabaseRepository


class ApiRepository:
    def __init__(self, db_repository: DatabaseRepository):
        self.db = db_repository

    async def select_user_table(self) -> Result[Union[record, List[record], int], str]:

        query = QueryModel(table=DatabaseTables.perfis)

        result = await self.db.select(query)

        if result.is_failure:
            return Failure("Erro ao coletada tabela de usuários", details=result.value)

        return Success(result.value, log="tabela coletada de usuario com sucesso")

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
