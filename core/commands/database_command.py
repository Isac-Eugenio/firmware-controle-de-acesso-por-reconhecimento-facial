from typing import List
from numpy import record
from core.commands.async_command import AsyncCommand
from core.commands.result import *
from models.query_model import QueryModel
from databases import Database as AsyncDatabase

class DatabaseCommand(AsyncCommand):

    def __init__(self, database: AsyncDatabase):
        self.database = database
        self.isconnected = False

    async def _connect_func(self) -> Result[str, str]:
        try:
            self.connection = await self.database.connect()
            self.isconnected = True
            return Success("Conexão bem-sucedida")
        except Exception as e:
            self.isconnected = False
            return Failure(f"Erro ao se conectar ao DB", details=str(e))

    async def _connect(self) -> Result[str, str]:
        result = await self.execute_async(self._connect_func)
        return result

    async def close(self):
        if self.connection:
            self.connection.close()
            await self.connection.wait_closed()
            self.isconnected = False


    async def _disconnect(self) -> Result[str, str]:
        if not self.isconnected:
            return Success("DB já desconectado")

        try:
            await self.database.disconnect()
            self.isconnected = False
            return Success("Desconexão bem-sucedida")
        except Exception as e:
            return Failure(f"Erro ao desconectar do DB", details=str(e))


    async def execute_query(self, query: QueryModel, type_fetch: str = None) -> Result[Union[record, List[record], int], str]:
        # Tenta conectar
        conn_result = await self._connect()
        if conn_result.is_failure:
            return Failure(f"Erro ao conectar ao banco de dados", details=conn_result.value)

        try:
            # Executa a query de acordo com o tipo
            if type_fetch == "one":
                data = await self.database.fetch_one(query=query.query, values=query.values)
            elif type_fetch == "all":
                data = await self.database.fetch_all(query=query.query, values=query.values)
            else:
                data = await self.database.execute(query=query.query, values=query.values)

            return Success(data)

        except Exception as e:
            return Failure(f"Erro ao executar a query", details=str(e))

        finally:
            # Desconecta sempre, mesmo se ocorrer erro
            await self._disconnect()

