from models.baseuser_model import BaseUserModel

class LoginModel(BaseUserModel):
   def set_credentials(self, email: str, senha: str) -> None:
      self.email = email
      self.senha = senha  # setter protegido

   def get_email(self) -> str:
      return self.email

   def get_senha(self) -> str:
      print(self.senha)