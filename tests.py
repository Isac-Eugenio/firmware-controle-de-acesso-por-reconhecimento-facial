from core.config.app_config import load_config
from models.baseuser_model import BaseUserModel

async def debug_async():
    pass


async def debug_stream():
    pass


def debug():
    model = BaseUserModel()
    teste = model.model_json_schema()

    print(teste)

if __name__ == "__main__":
    debug()
