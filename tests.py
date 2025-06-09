from pydantic import ValidationError
from core.config.app_config import load_config
from models.baseuser_model import BaseUserModel, PermissionLevel
from models.login_model import LoginModel


async def debug_async():
    pass


async def debug_stream():
    pass


def debug():
    data = {
        "email": "isac@exemplo.com",
        "senha": "123456789",
    }

    user = LoginModel.model_validate(data)

    print(user.email)  # isac@exemplo.com

    # Tentar acessar a senha direto lança erro
    try:
        print(user.senha)
    except Exception as e:
        print(e)  # A senha não pode ser acessada diretamente.

    # Verificar senha correta
    print(user.verificar_senha("123456789"))  # True
    print(user.verificar_senha("errada"))  # False


if __name__ == "__main__":
    debug()
