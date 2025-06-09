from models.baseuser_model import BaseUserModel

class LoginModel(BaseUserModel):
   def __init__(self):
      super().__init__()
      self._email: str = ""
      self._senha: str = ""

   def set_credentials(self, email: str, senha: str) -> None:
      self._email = email
      self._senha = senha
    