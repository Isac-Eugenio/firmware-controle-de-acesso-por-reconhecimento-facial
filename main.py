
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi import FastAPI

import asyncio
import json

from controllers.api_controller import ApiController
from core.commands.stream_command import StreamCommand
from core.config.app_config import CameraConfig
from models.login_model import LoginModel
from models.stream_response_model import StreamResponse
from models.user_model import UserModel
from repository.api_repository import ApiRepository
from repository.camera_repository import CameraRepository
from repository.database_repository import DatabaseRepository
from services.face_service import FaceService
from models.response_model import Response

camera_repository = CameraRepository(CameraConfig())

db_repository = DatabaseRepository()

face_service = FaceService(camera_repository)

api_repository = ApiRepository(db_repository)

api = ApiController(api_repository, face_service)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/login")
async def login(request: Request):
    formulario = await request.json()

    result = await api.login(formulario)

    if result.is_success:

        data_dict = result.value.model_dump()

        response = Response(
            log="Login realizado com sucesso ...",
            data=data_dict,
            code=200,
        )
        return response.json()

    if result.is_failure:
        if result.details is None:
            response = Response(log="Acesso Negado ...", code=401)
            return response.json()

        response = Response(
            log="Erro ao realizar login ..",
            details=result.details,
            error=result.value,
            code=500,
        )
        return response.json()


@app.post("/perfis")
async def table_perfil(request: Request):
    formulario = await request.json()

    model = LoginModel(**formulario)

    auth = await api.isAdmin(model)

    print(auth)

    if auth.value:
        result = await api.get_user_table()

        if result.is_failure:
            response = Response(code=500, log=result.value, details=result.details)
            return response.json()

        response = Response(code=200, data=result.value, log=result.log)
        return response.json()

    if auth.is_failure:
        response = Response(code=500, log=auth.value, details=auth.details)
        return response.json()

    response = Response(code=401, log="Acesso Negado ...", details=auth.log)
    return response.json()


async def json_stream(form):
    for i in range(5):  # <-- for normal
        data = {"evento": i, "mensagem": f"Mensagem numero {i} {form}"}
        yield json.dumps(data)
        await asyncio.sleep(1)


# --- Endpoint que envia via SSE ---
@app.post("/register_user")
async def register_user(request: Request):

    form = await request.json()

    command = StreamCommand(lambda: json_stream(form))

    res = StreamResponse(command)

    return await res.response()


"""
@app.post('/auth_entrada')
async def verificar_entrada(request: requests.Request):
    async def event_generator():
        try:
            async for step in api._validate_user(
                columns=["nome", "email", "alias"],
                encoding_column="encodings",  
                table="usuarios",
                trust=60
            ):
                if not step["final"]:
                    yield f"data: {step['message']}\n\n"
                    
                else:
                    if "data" in step and step["data"]:
                        yield json.dumps(step["data"])
                    else:
                        yield json.dumps(step["message"])

                
        except Exception as e:
            yield f"data: Erro ao processar: {str(e)}\n\n"
    
    return responses.StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post('/new_perfil')
async def new_perfil(request: requests.Request):
    req = await request.json()
    
    async def event_generator():
            try:
                async for step in api._insert_user(
                    data=req,
                    encoding_column="encodings",  
                    table="usuarios"
                ):
                    if not step["final"]:
                        yield f"data: {step['message']}\n\n"
                        
                    else:
                        yield f"Resultado: {step['message']}\n\n"

                    
            except Exception as e:
                yield f"data: Erro ao processar: {str(e)}\n\n"
    
    return responses.StreamingResponse(event_generator(), media_type="text/event-stream")
# Area de testes via rede:

@app.get("/debug")
async def debug():
    async def event_generator():
        try:
            async for step in api._validate_user(
                columns=["nome", "email", "alias"],
                encoding_column="encodings",  
                table="usuarios",
                trust=60
            ):
                yield f"data: {step['message']}\n\n"
        except Exception as e:
            yield f"data: Erro ao processar: {str(e)}\n\n"

    return responses.StreamingResponse(event_generator(), media_type="text/event-stream")

"""
