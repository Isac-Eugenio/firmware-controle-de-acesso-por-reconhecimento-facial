from typing import Any, Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class Response:
    def __init__(
        self,
        code: int,
        log: str,
        error: Optional[str] = None,
        details: Optional[str] = None,
        data: Optional[Any] = None,
    ):
        self.code = code
        self.log = log
        self.error = error
        self.details = details
        self.data = data

    def json(self) -> JSONResponse:
        return JSONResponse(
            content=jsonable_encoder(self.__dict__),
            status_code=self.code,
            headers={"Content-Type": "application/json"},
        )
