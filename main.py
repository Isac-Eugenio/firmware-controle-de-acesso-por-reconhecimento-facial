from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, requests, responses, websockets
import json

from controllers.api_controller import ApiController
from core.config.app_config import CameraConfig
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
async def login(request: requests.Request):
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
            response = Response(log="Acesso Negado ...", code=200)
            return response.json()

        response = Response(
            log="Erro ao realizar login ..",
            details=result.details,
            error=result.value,
            code=400,
        )
        return response.json()


"""
@app.post('/tabela_perfis')
async def table_perfil(request: requests.Request):
    formulario = await request.json()
    
    auth = await api._verify_user(data=formulario)
    result = dict(auth)
    print(result)
    
    if result.get("auth", True):  # Verificando se a autenticação foi bem-sucedida
        list_result = []
        api_service = ApiService()
        api_result = await api_service._get_table(columns=["nome", "alias", "email", "permission_level", "matricula"], table="usuarios")

        for row in api_result['result']:
            list_result.append(dict(row))   
    return {"error": None, "tabela": []}

    return responses.JSONResponse(
        content={"error": "Erro ao ler as tabelas de perfis", "tabela": []},
        status_code=400  # Código de status adequado para falha na leitura da tabela
    )


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
