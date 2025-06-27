import bcrypt
from core.config.app_config import PerfisColumns
from models.baseuser_model import BaseUserModel


class UserModel(BaseUserModel):
    def __init_subclass__(cls, **kwargs):
        return super().__init_subclass__(**kwargs)
