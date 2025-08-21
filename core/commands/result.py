from __future__ import annotations
from abc import ABC
from dataclasses import asdict, dataclass, is_dataclass
from typing import Generic, TypeVar, Callable, Union

TSuccess = TypeVar("TSuccess")
TFailure = TypeVar("TFailure")
TNew = TypeVar("TNew")


class Result(ABC, Generic[TSuccess, TFailure]):

    @property
    def value(self) -> Union[TSuccess, TFailure, None]:
        if isinstance(self, Success):
            return self._value
        elif isinstance(self, Failure):
            return self._value
        elif isinstance(self, Running):
            return self._value
        return None

    @property
    def typeValue(self) -> Result:
        return self

    @property
    def is_success(self) -> bool:
        return isinstance(self, Success)

    @property
    def is_failure(self) -> bool:
        return isinstance(self, Failure)

    @property
    def is_running(self) -> bool:
        return isinstance(self, Running)

    @property
    def success_or_none(self) -> TSuccess | None:
        return self._value if isinstance(self, Success) else None

    @property
    def failure_or_none(self) -> TFailure | None:
        return self._value if isinstance(self, Failure) else None

    @property
    def running_or_none(self) -> TSuccess | None:
        return self._value if isinstance(self, Running) else None

    def fold(
        self,
        on_success: Callable[[TSuccess], TNew],
        on_failure: Callable[[TFailure], TNew],
        on_running: Callable[[TSuccess], TNew] | None = None,
    ) -> TNew:
        if isinstance(self, Success) and on_running is None:
            return on_success(self._value)
        elif isinstance(self, Running) and on_running is not None:
            return on_running(self._value)
        elif isinstance(self, Failure):
            return on_failure(self._value)
        else:
            raise ValueError("Unhandled state in fold")

    def map(self, func: Callable[[TSuccess], TNew]) -> Result[TNew, TFailure]:
        if isinstance(self, Success):
            return Success(func(self._value))
        elif isinstance(self, Running):
            return Running(func(self._value))
        else:  # Failure
            return Failure(self._value)

    def map_failure(self, func: Callable[[TFailure], TNew]) -> Result[TSuccess, TNew]:
        if isinstance(self, Failure):
            return Failure(func(self._value))
        elif isinstance(self, Running):
            return Running(self._value)
        else:  # Success
            return Success(self._value)

    def __repr__(self) -> str:
        if isinstance(self, Success):
            return f"Success({self._value})"
        elif isinstance(self, Failure):
            return f"Failure({self._value})"
        elif isinstance(self, Running):
            return f"Running({self._value})"
        return "UnknownResult()"

    def to_map(self) -> dict:
        if is_dataclass(self):
            return asdict(self)
        return {"_value": getattr(self, "_value", None)}

@dataclass(frozen=True)
class Success(Result[TSuccess, TFailure]):
    _value: TSuccess
    details: str = None
    log: str = None


@dataclass(frozen=True)
class Failure(Result[TSuccess, TFailure]):
    _value: TFailure
    details: str = None
    log: str = None


@dataclass(frozen=True)
class Running(Result[TSuccess, TFailure]):
    _value: TSuccess
