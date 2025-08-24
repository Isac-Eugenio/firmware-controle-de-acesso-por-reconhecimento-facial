from typing import AsyncGenerator, Callable, Optional

from core.commands.async_command import AsyncCommand
from core.commands.result import *

class StreamCommand(AsyncCommand[TSuccess, TFailure]):
    async def execute_stream(
        self,
        stream: Optional[Callable[[], AsyncGenerator[Result[TSuccess, TFailure], None]]] = None,
    ) -> AsyncGenerator[Result[TSuccess, TFailure], None]:
        if stream is not None:
            self._function = stream

        if self._function is None:
            raise ValueError("Nenhuma função fornecida para execução do AsyncCommand.")

        try:
            async for task in self._function():
                yield task

        except Exception as e:
            self.result = Failure(e)
            yield self.result
