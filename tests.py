from core.config.app_config import load_config
from models.baseuser_model import BaseUserModel
from models.login_model import LoginModel

async def debug_async():
    pass


async def debug_stream():
    pass


def debug():
    model = LoginModel()
    model.set_credentials(email="isaceugenio564@gmail.com", senha="123")

    teste = model.get_credentials()
    
    print(teste)

if __name__ == "__main__":
    debug()
