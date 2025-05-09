from core.config.config import config
from databases import Database as AsyncDatabase

DATABASE_URL = "mysql+aiomysql://{}:{}@{}:{}/{}".format(
    config["credentials"]["database"]["user"],
    config["credentials"]["database"]["password"],
    config["hosts"]["database"],
    config["ports"]["database"],
    config["credentials"]["database"]["name"]
)

class Database:
    def __init__(self, database_url=None):
        self.database_url = database_url or DATABASE_URL
        self.database = AsyncDatabase(self.database_url)
        self.isconnected = {"log": "ainda não conectado ao Banco de Dados", "status": False}
        self.isquery = lambda x: False if x is None else True

    async def _connect(self):
        if not self.isconnected["status"]:
            try:
                await self.database.connect()
                self.isconnected = {"log": "conectado ao Banco de Dados", "status": True}
            except Exception as e:
                self.isconnected = {"log": f"erro ao conectar ao Banco de Dados: {e}", "status": False}
                raise Exception(f"Erro ao conectar ao banco de dados: {e}")

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
        columns = ", ".join(data.keys())
        values = ", ".join([f"= {value}" for value in data.values()])
        query = f"INSERT INTO {table} ({columns}) VALUES ({values})"

        result = await self._execute_query(query=query, values=data)
        await self._disconnect()

        return {
            "log": self.isconnected,
            "result": result,
            "status": self.isquery(result),
            "query": query
        }

    async def update(self, table: str, data: dict, condition: str):
        await self._ensure_connected()
        set_clause = ", ".join([f"{key} = :{key}" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"

        result = await self._execute_query(query=query, values=data)
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
