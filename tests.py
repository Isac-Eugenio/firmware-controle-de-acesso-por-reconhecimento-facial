from pydantic import ValidationError
from core.config.app_config import load_config
from models.baseuser_model import BaseUserModel, PermissionLevel
from models.login_model import LoginModel

async def debug_async():
    pass


async def debug_stream():
    pass


def debug():
    # Simulando o form_data
    form_data = {
        "email": "isac@exemplo.com",
        "senha": "123456789",
    }

    # Cria o login model com validação para o campo email
    try:
        login = LoginModel.model_validate(form_data)
    except ValidationError as e:
        print("Erro de validação:", e)
        exit(1)

    print(login.model_dump_json())

   
if __name__ == "__main__":
    debug()
