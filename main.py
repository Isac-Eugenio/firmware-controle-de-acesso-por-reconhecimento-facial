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
    print(f'request: {formulario}')
    
    result = await service.login()
    
    return responses.JSONResponse(
            content=result,
            status_code=200
        )

@app.post('/tabela_perfis')
async def table_perfil(request: requests.Request):
   formulario = await request.json()
   service = LoginService(form=formulario)
   print(f'request: {formulario}')
    
   result = await service.login()
 
   if result['auth']:
        list_result = []
        service = ApiService()
        result = await service.get_table(columns=["nome", "email", "auth", "matricula"],table="usuarios")
        for i in result['result']:
            list_result.append(dict(i))
        return {"error": None, "tabela": list_result}
   
   else:
       return {"error": "Erro ao ler as tabelas de perifis", 
               "tabela": []}
   
   
@app.get("/debug")

async def debug():
    face = api_tools._extract_valid_face_encoding()
    print(face)
    return responses.JSONResponse(
        content={
            "message": "Debug successful",
            "data": face
        },
        status_code=200
    )
