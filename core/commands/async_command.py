from typing import Optional, Callable, Union, Awaitable
from core.commands.command import Command
from core.commands.result import Result, Failure, TSuccess, TFailure


class AsyncCommand(Command[TSuccess, TFailure]):
    async def execute_async(
        self,
        function: Optional[Callable[[], Awaitable[Result[TSuccess, TFailure]]]] = None,
    ) -> Result[TSuccess, TFailure]:
        if function is not None:

            async def wrapper():
                return await function()

            self._function = wrapper

        if self._function is None:
            raise ValueError("Nenhuma função fornecida para execução do AsyncCommand.")

        try:
            self.result = await self._function()
        except Exception as e:
            self.result = Failure(
                _value=str(e),
                details=getattr(e, "args", None),
                log="Erro no AsyncCommand",
            )

        return self.result

    async def execute_async_with_param(
        self,
        param: object,
        function: Optional[
            Callable[[object], Awaitable[Result[TSuccess, TFailure]]]
        ] = None,
    ) -> Result[TSuccess, TFailure]:
        if function is not None:
            # Cria uma async wrapper que retorna a coroutine corretamente
            async def wrapper():
                return await function(param)

            self._function = wrapper

        if self._function is None:
            raise ValueError("Nenhuma função fornecida para execução do AsyncCommand.")

        try:
            self.result = await self._function()
        except Exception as e:
            self.result = Failure(
                _value=str(e),
                details=getattr(e, "args", None),
                log="Erro no AsyncCommand",
            )

        return self.result
