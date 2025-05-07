from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, requests, responses
from services.login_service import LoginService
from services.face_service import FaceService
from services.api_service import ApiService

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
    print(f'Request: {formulario}')

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

   
@app.get("/debug")
async def debug():
    try:
        face = api_tools._extract_valid_face_encoding()  # Chama o serviço para extrair a face
        if face:
            return responses.JSONResponse(
                content={"message": "Debug bem-sucedido", "data": face},
                status_code=200
            )
        else:
            return responses.JSONResponse(
                content={"error": "Nenhuma face válida encontrada", "data": []},
                status_code=404
            )
    except Exception as e:
        print(f"Erro durante o debug: {e}")
        return responses.JSONResponse(
            content={"error": f"Erro ao processar: {str(e)}", "data": []},
            status_code=500  # Código de status adequado para erro interno do servidor
        )

