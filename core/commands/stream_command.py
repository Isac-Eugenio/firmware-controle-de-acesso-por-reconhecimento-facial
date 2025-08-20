from typing import AsyncGenerator, Awaitable, Callable, Optional
from core.commands.async_command import AsyncCommand
from core.commands.command import TFailure, TSuccess
from core.commands.result import *


class StreamCommand(AsyncCommand[TSuccess, TFailure]):
    async def execute_stream(
        self,
        stream: Optional[Callable[[], Awaitable[Result[TSuccess, TFailure]]]] = None,
    ) -> AsyncGenerator[Result[TSuccess, TFailure], None]:
        if stream is not None:
            self._function = stream

        if self._function is None:
            raise ValueError("Nenhuma função fornecida para execução do AsyncCommand.")

        try:
            async for task in self._function():

                if isinstance(task, Running):
                    self.result = task
                    yield self.result
                    continue

                if isinstance(task, Failure):
                    self.result = task
                    yield self.result
                    break

                if isinstance(task, Success):
                    self.result = task
                    yield self.result
                    break

        except Exception as e:
            self.result = Failure(e)
            yield self.result
