from fastapi.responses import StreamingResponse
from core.commands.stream_command import StreamCommand
import json


class StreamResponse:
    def __init__(self, stream_command: StreamCommand):
        self.stream = stream_command

    async def _def_generator(self):
        async for task in self.stream.execute_stream():
            yield f"{task.to_map()}\n\n"

    async def response(self) -> StreamingResponse:
        return StreamingResponse(self._def_generator(), media_type="text/event-stream")
