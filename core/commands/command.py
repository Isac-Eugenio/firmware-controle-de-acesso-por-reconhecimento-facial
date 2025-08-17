from abc import ABC
from typing import Callable, Generic, Optional, TypeVar, Union
from core.commands.result import Result, Success, Failure

TSuccess = TypeVar("TSuccess")
TFailure = TypeVar("TFailure")


class Command(ABC, Generic[TSuccess, TFailure]):
    def __init__(
        self, function: Optional[Callable[[], Result[TSuccess, TFailure]]] = None
    ):
        self._function: Optional[Callable[[], Result[TSuccess, TFailure]]] = function
        self.result: Optional[Result[TSuccess, TFailure]] = None

    def execute(
        self, function: Optional[Callable[[], Result[TSuccess, TFailure]]] = None
    ) -> Result[TSuccess, TFailure]:

        if function is not None:
            self._function = function

        if self._function is None:
            raise ValueError("Nenhuma função fornecida para execução do Command.")

        try:
            self.result = self._function()
        except Exception as e:
            self.result = Failure(e)

        return self.result

    def execute_with_param(
        self, param: Union[object],
        function: Optional[Callable[[], Result[TSuccess, TFailure]]] = None
    ) -> Result[TSuccess, TFailure]:

        if function is not None:
            self._function = function(param)

        if self._function is None:
            raise ValueError("Nenhuma função fornecida para execução do Command.")

        try:
            self.result = self._function(param)

        except Exception as e:
            self.result = Failure(e)

        return self.result
