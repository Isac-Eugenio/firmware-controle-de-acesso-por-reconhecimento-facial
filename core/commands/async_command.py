from typing import Optional, Callable, Union, Awaitable
from core.commands.command import Command
from core.commands.result import Result, Failure, TSuccess, TFailure

class AsyncCommand(Command[TSuccess, TFailure]):
    async def execute_async(
        self,
        function: Optional[Callable[[], Awaitable[Result[TSuccess, TFailure]]]] = None
    ) -> Result[TSuccess, TFailure]:
        if function is not None:
            self._function = function

        if self._function is None:
            raise ValueError("Nenhuma função fornecida para execução do AsyncCommand.")

        try:
            self.result = await self._function()
        except Exception as e:
            self.result = Failure(e)

        return self.result

    async def execute_async_with_param(
        self,
        param: object,
        function: Optional[Callable[[object], Awaitable[Result[TSuccess, TFailure]]]] = None,
    ) -> Result[TSuccess, TFailure]:
        if function is not None:
            # Armazena uma função que recebe param, sem executar ainda
            self._function = lambda p=param: function(p)

        if self._function is None:
            raise ValueError("Nenhuma função fornecida para execução do AsyncCommand.")

        try:
            self.result = await self._function()
        except Exception as e:
            self.result = Failure(e)

        return self.result
