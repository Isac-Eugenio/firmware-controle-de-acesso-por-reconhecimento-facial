from databases import Database as AsyncDatabase

from core.errors.database_exception import *
from .response_repository import RepositoryResponse
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
    def __init__(self, database_url=None, user_model: UserModel=None):
        self.model = user_model
        self.database_url = database_url or DATABASE_URL
        self.database = AsyncDatabase(self.database_url)
        self.isconnected = RepositoryResponse(status=False, log="Banco ainda não conectado")
        self.isquery = lambda x: False if x is None else True

    async def _connect(self):
        if not self.isconnected.status:
            try:
                await self.database.connect()
                self.isconnected = RepositoryResponse(status=True, log="Conexão ao DB bem-sucessida !")
            except Exception as e:
                self.isconnected = RepositoryResponse(status=False, log="Erro ao conectar ao DB !")
                raise DatabaseConnectionError(f"Erro ao conectar ao banco de dados: {e}")

    async def _disconnect(self):
        if self.isconnected["status"]:
            try:
                await self.database.disconnect()
                self.isconnected = {"log": "Banco de Dados desconectado com sucesso", "status": False}
            except Exception as e:
                self.isconnected = {"log": f"erro ao desconectar do Banco de Dados: {e}", "status": False}
                raise Exception(f"Erro ao desconectar do banco de dados: {e}")
        else:
            self.isconnected = {"log": "já desconectado do Banco de Dados", "status": False}

    """  
    
    TODO: Manutenção -- Atualizando repositório
    
    async def _ensure_connected(self):
        if not self.isconnected["status"]:
            await self._connect()

    async def _execute_query(self, query, values=None, type_fetch=None):
        try:
            if type_fetch == "one":
                return await self.database.fetch_one(query=query, values=values)
            elif type_fetch == "all":
                return await self.database.fetch_all(query=query, values=values)
            else:
                return await self.database.execute(query=query, values=values)
        except Exception as e:
            raise Exception(f"Erro de Query: {e}")
    
    async def select_one(self, columns=None, condition=None, table: str = None, values=None):
        await self._ensure_connected()

        if columns is None:
            columns = "*"
        else:
            columns = ", ".join(columns)

        query = f"SELECT {columns} FROM {table}"
        if condition:
            query += f" WHERE {condition}"

        result = await self._execute_query(query=query, values=values, type_fetch="one")

        await self._disconnect()

        return {
            "log": self.isconnected,
            "result": result,
            "status": self.isquery(result),
            "query": query
        }


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