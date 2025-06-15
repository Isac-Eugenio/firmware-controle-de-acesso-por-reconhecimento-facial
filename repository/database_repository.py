from databases import Database as AsyncDatabase

from core.errors.database_exception import *
from models.query_model import QueryModel
from models.response_model import ResponseModel
from core.config.app_config import DatabaseConfig as db

DATABASE_URL = "mysql+aiomysql://{}:{}@{}:{}/{}".format(
    db.user, db.password, db.host, db.port, db.name
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
                raise DatabaseConnectionError(
                    "Erro ao se conectar ao DB!", details=str(e)
                ) from e

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
                raise DatabaseConnectionError(
                    "Erro ao desconectar do DB!", details=str(e)
                ) from e
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
                raise DatabaseConnectionError(
                    "Erro ao tentar reconectar ao DB!", details=str(e)
                ) from e

    async def _execute_query(self, query: QueryModel, type_fetch=None):
        try:
            if type_fetch == "one":
                return await self.database.fetch_one(
                    query=query.query, values=query.values
                )
            elif type_fetch == "all":
                return await self.database.fetch_all(
                    query=query.query, values=query.values
                )
            else:
                return await self.database.execute(
                    query=query.query, values=query.values
                )
        except Exception as e:
            raise DatabaseQueryError("Erro ao executar a query", details=str(e)) from e

    async def select_one(self, query: QueryModel):
        try:
            await self._ensure_connected()
            query.select()

            result = await self._execute_query(query=query, type_fetch="one")
            await self._disconnect()

            return ResponseModel(
                status=True, log="Query executada com sucesso", data=result, error=False
            )

        except DatabaseException as e:
            await self._disconnect()
            return ResponseModel(
                status=True,
                log="Erro ao se Comunicar ao DB",
                details=e.details,
                error=True,
            )

        except Exception as e:
            await self._disconnect()
            raise DatabaseQueryError("Erro ao executar query", details=str(e)) from e

    async def select(self, query: QueryModel):
        try:
            await self._ensure_connected()
            query.select()

            result = await self._execute_query(query=query, type_fetch="all")
            await self._disconnect()

            return ResponseModel(
                status=True, log="Query executada com sucesso", data=result, error=False
            )

        except DatabaseException as e:
            await self._disconnect()
            return ResponseModel(
                status=True,
                log="Erro ao se Comunicar ao DB",
                details=e.details,
                error=True,
            )

        except Exception as e:
            await self._disconnect()
            raise DatabaseQueryError("Erro ao executar query", details=str(e)) from e

    async def insert(self, query: QueryModel):
        try:
            await self._ensure_connected()

            query.insert()

            result = await self._execute_query(query=query)

            await self._disconnect()

            return ResponseModel(
                status=True, error=False, log="Query executada com Sucesso", data=result
            )

        except DatabaseException as e:
            await self._disconnect()
            return ResponseModel(
                status=True, error=True, log="Erro ao Executar Query", details=str(e)
            )

        except Exception as e:
            await self._disconnect()
            raise DatabaseQueryError("Erro ao executar query", details=str(e)) from e

    async def delete(self, query: QueryModel):
        try:
            await self._ensure_connected()
            query.delete()

            result = await self._execute_query(query=query)

            await self._disconnect()

            return ResponseModel(
                status=True,
                log="Delete executado com sucesso",
                data=result,
                error=False,
            )

        except DatabaseException as e:
            await self._disconnect()
            return ResponseModel(
                status=True,
                log="Erro ao executar DELETE",
                details=e.details,
                error=True,
            )

        except Exception as e:
            await self._disconnect()
            raise DatabaseQueryError("Erro ao executar DELETE", details=str(e)) from e

    async def update(self, query: QueryModel, new_query: QueryModel):
        try:
            await self._ensure_connected()
            query.update(new_query)

            result = await self._execute_query(query=query)

            await self._disconnect()

            match result:
                case 1:
                    return ResponseModel(
                        status=True,
                        log="Update executado com sucesso",
                        data=result,
                        error=False,
                    )

                case 0:
                    return ResponseModel(
                        status=True,
                        log="Nenhum dado correspondente",
                        data=result,
                        error=False,
                    )

                case _:
                    return ResponseModel(
                        status=True,
                        log="Mas de um dado Atualizado",
                        data=result,
                        error=False,
                    )

        except DatabaseException as e:
            await self._disconnect()
            return ResponseModel(
                status=True,
                log="Erro ao executar UPDATE",
                details=e.details,
                error=True,
            )

        except Exception as e:
            await self._disconnect()
            raise DatabaseQueryError("Erro ao executar UPDATE", details=str(e)) from e

    async def count(self, query: QueryModel):
        try:
            await self._ensure_connected()
            query.count()

            result = await self._execute_query(query=query, type_fetch="one")

            await self._disconnect()

            return ResponseModel(
                status=True,
                log="Contagem executada com sucesso",
                data=result,
                error=False,
            )

        except DatabaseException as e:
            await self._disconnect()
            return ResponseModel(
                status=True, log="Erro ao executar COUNT", details=e.details, error=True
            )

        except Exception as e:
            await self._disconnect()
            raise DatabaseQueryError("Erro ao executar COUNT", details=str(e)) from e
