from databases import Database as AsyncDatabase

from core.errors.database_exception import *
from models.dataclass.query_model import QueryModel
from models.dataclass.response_model import ResponseModel
from core.config.app_config import config
from models.user_model import UserModel

DATABASE_URL = "mysql+aiomysql://{}:{}@{}:{}/{}".format(
    config["credentials"]["database"]["user"],
    config["credentials"]["database"]["password"],
    config["hosts"]["database"],
    config["ports"]["database"],
    config["credentials"]["database"]["name"]
)


class DatabaseRepository:
    def __init__(self, database_url=None):
        self.database_url = database_url or DATABASE_URL
        self.database = AsyncDatabase(self.database_url)
        self.isconnected = ResponseModel(
            status=False, log="Banco ainda não conectado", error=False
        )
        self.isquery = lambda x: False if x is None else True

    async def _connect(self):
        if not self.isconnected.status:
            try:
                await self.database.connect()
                self.isconnected = ResponseModel(
                    status=True, log="Conexão ao DB bem-sucedida!", error=False
                )
            except Exception as e:
                self.isconnected = ResponseModel(
                    status=False, log="Erro ao conectar ao DB!", error=True
                )
                raise DatabaseConnectionError("Erro ao se conectar ao DB!", details=str(e)) from e

    async def _disconnect(self):
        if self.isconnected.status:
            try:
                await self.database.disconnect()
                self.isconnected = ResponseModel(
                    status=True, log="Desconexão do DB bem-sucedida!", error=False
                )
            except Exception as e:
                self.isconnected = ResponseModel(
                    status=False, log="Erro ao desconectar do DB!", error=True
                )
                raise DatabaseConnectionError("Erro ao desconectar do DB!", details=str(e)) from e
        else:
            self.isconnected = ResponseModel(
                status=True, log="DB já desconectado!", error=False
            )

    async def _ensure_connected(self):
        if not self.isconnected.status:
            try:
                await self._connect()
            except DatabaseException:
                raise
            except Exception as e:
                raise DatabaseConnectionError("Erro ao tentar reconectar ao DB!", details=str(e)) from e

    async def _execute_query(self, query: QueryModel, type_fetch=None):
        try:
            if type_fetch == "one":
                return await self.database.fetch_one(query=query.query, values=query.values)
            elif type_fetch == "all":
                return await self.database.fetch_all(query=query.query, values=query.values)
            else:
                return await self.database.execute(query=query.query, values=query.values)
        except Exception as e:
            raise DatabaseQueryError("Erro ao executar a query", details=str(e)) from e

    async def select_one(self, query: QueryModel):
        try:
            await self._ensure_connected()
            query_sql = query.select()  # monta a SQL string
            result = await self._execute_query(query=query_sql, type_fetch="one")
            await self._disconnect()

            return ResponseModel(
                status=True,
                log="Query executada com sucesso",
                data=result
            )

        except DatabaseException as e:
            await self._disconnect()
            return ResponseModel(
                status=False,
                log="Erro ao se Comunicar ao DB",
                details=e.details,
                error=True
            )

        except Exception as e:
            await self._disconnect()
            raise DatabaseQueryError("Erro ao executar query", details=str(e)) from e

    """  
    TODO: Manutenção -- Atualizando repositório

    async def select(self, columns=None, condition=None, table: str = None, values=None):
        await self._ensure_connected()

        if columns is None:
            columns = "*"
        else:
            columns = ", ".join(columns)

        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"

        result = await self._execute_query(query=query, values=values, type_fetch="all")

        await self._disconnect()

        return {
            "log": self.isconnected,
            "result": result,
            "status": self.isquery(result),
            "query": query
        }

    async def insert(self, table: str, data: dict):
        await self._ensure_connected()

        # Gerar as colunas a partir das chaves do dicionário 'data'
        columns = ", ".join(data.keys())

        # Criar os placeholders nomeados (usando :coluna)
        placeholders = ", ".join([f":{key}" for key in data.keys()])

        # Construção da query
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

        # Passar o dicionário de dados como valores para os placeholders
        values = data

        try:
            # Executando a consulta passando os dados como parâmetros
            result = await self._execute_query(query=query, values=values)
        except Exception as e:
            result = None
            Exception(e)

        await self._disconnect()

        return {
            "log": self.isconnected,
            "result": result,
            "status": self.isquery(result),
            "query": query
        }


    async def delete(self, table: str, condition: str):
        await self._ensure_connected()
        query = f"DELETE FROM {table} WHERE {condition}"

        result = await self._execute_query(query=query)
        await self._disconnect()

        return {
            "log": self.isconnected,
            "result": result,
            "status": self.isquery(result),
            "query": query
        }

    async def count(self, table: str, condition=None):
        await self._ensure_connected()
        query = f"SELECT COUNT(*) as result FROM {table}"
        if condition:
            query += f" WHERE {condition}"

        result = await self._execute_query(query=query, type_fetch="one")
        await self._disconnect()

        return {
            "log": self.isconnected,
            "result": result,
            "status": self.isquery(result),
            "query": query
        }

    async def close(self):
        if self.isconnected["status"]:
            await self._disconnect()
        else:
            print("Banco de Dados já desconectado!")
            self.isconnected = {"log": "já desconectado do Banco de Dados", "status": False}
 """