import hashlib
import random

import hashlib
import random
from typing import AsyncGenerator, Awaitable, Callable, List, Tuple

from models.response_model import ResponseModel
from repository.database_repository import DatabaseRepository


class ApiUtils:
    @staticmethod
    def _generate_id() -> str:
        return str(random.randint(0, 99999999)).zfill(8)

    @staticmethod
    def _ensure_str_values(data: dict) -> dict:
        return {key: f"'{value}'" for key, value in data.items()}

    @staticmethod
    def is_empty_list(lst) -> list:
        return [] if not lst else lst

    @staticmethod
    def _hash_sha256(s: str) -> str:
        return hashlib.sha256(s.encode("utf-8")).hexdigest()

    @staticmethod
    def _is_sha256_hash(s: str) -> bool:
        if len(s) != 64:
            return False
        try:
            int(s, 16)  # testa se é hexadecimal
            return True
        except ValueError:
            return False

    @staticmethod
    def _limpar_dict(d: dict) -> dict:
        return {k: v for k, v in d.items() if v not in ("", None, [], {})}

    @staticmethod
    def _null_or_empty_columns(d: dict) -> list[str]:
        return [k for k, v in d.items() if v in ("", None, [], {})]

    @staticmethod
    async def _execute_task(
        tasks: List[Tuple[str, Callable[[], AsyncGenerator[ResponseModel, None]]]],
        db_rep: DatabaseRepository,
    ) -> AsyncGenerator[ResponseModel, None]:
        try:
            await db_rep._connect()

            for etapa, (nome, task) in enumerate(tasks):
                # task() retorna um async generator, iteramos nele:
                async for mensagem in task():
                    if mensagem.error:
                        yield ResponseModel(
                            status=False,
                            log=str(mensagem.details),
                            data=None,
                            error=True,
                            details=f"❌ Erro na função [{etapa}] [{nome}]: {mensagem.log}",
                        )
                        # Sai da execução ao encontrar erro na tarefa
                        break
                    else:
                        yield ResponseModel(
                            status=False,  # status False durante a execução
                            log=str(etapa),
                            data=mensagem,
                            error=False,
                            details=f"✅ Função [{etapa}] [{nome}] executada: {mensagem.log}",
                        )
                else:
                    # Esse else é do for async: executa se não teve break
                    continue
                # Se houve break no for async (erro), interrompe o loop externo
                break
            else:
                # Executou todas as tarefas sem erro
                yield ResponseModel(
                    status=True,
                    log="✅ Todas as funções executadas com sucesso",
                    data=True,
                    error=False,
                )

        except Exception as e:
            yield ResponseModel(
                status=False,
                log="❌ Erro inesperado ao executar as tarefas",
                details=str(e),
                error=True,
            )
        finally:
            await db_rep._disconnect()