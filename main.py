from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, requests, responses, websockets
from services.login_service import LoginService
from services.face_service import FaceService
from services.api_service import ApiService
import json

api_tools = FaceService()
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
    service = LoginService(form=formulario)

    result = await service.login()

    if result.get("auth", False):  # Verificando se a autenticação foi bem-sucedida
        return responses.JSONResponse(
            content={"message": "Login bem-sucedido", "data": result},
            status_code=200
        )
    else:
        return responses.JSONResponse(
            content={"error": "Falha na autenticação"},
            status_code=401  # Código de status adequado para falha de autenticação
        )


@app.post('/tabela_perfis')
async def table_perfil(request: requests.Request):
    formulario = await request.json()
    service = LoginService(form=formulario)
    print(f'Request: {formulario}')

    result = await service.login()

    if result.get("auth", False):  # Verificando se a autenticação foi bem-sucedida
        list_result = []
        api_service = ApiService()
        api_result = await api_service.get_table(columns=["nome", "email", "auth", "matricula"], table="usuarios")

        for row in api_result['result']:
            list_result.append(dict(row))

        return {"error": None, "tabela": list_result}

    return responses.JSONResponse(
        content={"error": "Erro ao ler as tabelas de perfis", "tabela": []},
        status_code=400  # Código de status adequado para falha na leitura da tabela
    )


@app.post('/auth_entrada')
async def verificar_entrada(request: requests.Request):
    async def event_generator():
        try:
            async for step in api_tools._validate_user(
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

@app.post('/novo_usuario')
async def novo_usuario(request: requests.Request):
    pass

# Area de testes via rede:

@app.get("/debug")
async def debug():
    async def event_generator():
        try:
            async for step in api_tools._validate_user(
                columns=["nome", "email", "alias"],
                encoding_column="encodings",  
                table="usuarios",
                trust=60
            ):
                yield f"data: {step['message']}\n\n"
        except Exception as e:
            yield f"data: Erro ao processar: {str(e)}\n\n"

    return responses.StreamingResponse(event_generator(), media_type="text/event-stream")


