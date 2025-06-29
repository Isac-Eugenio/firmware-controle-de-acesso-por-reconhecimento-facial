""" from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, requests, responses, websockets
from services.login_service import LoginService
from services.user_service import ApiService
import json

app = FastAPI()
api = ApiService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],  
)

@app.post("/login")
async def login(request: requests.Request):
    try:
        formulario = await request.json()
        print(formulario)

        service = LoginService(form=formulario)
        result = await service.login()
        print(result)
        if result.get("auth", False): 
            return responses.JSONResponse(
                content={"message": "Login bem-sucedido", "data": result},
                status_code=200
            )
        else:
            return responses.JSONResponse(
                content={"message": "Acesso Negado", "data": result},
                status_code=200
            )
    
    except Exception as e:
        print(f"Erro ao processar o login: {str(e)}")
        return responses.JSONResponse(
            content={"message": "Erro interno do servidor", "error": str(e)},
            status_code=500
        )



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