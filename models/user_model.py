from models.face_model import FaceModel


class UserModel:
    def __init__(self):
        self.nome = ""
        self.email = ""
        self.matricula = ""
        self.alias = ""
        self.cpf = ""
        self.id = ""
        self._senha = ""
        self._face_model = FaceModel()
        
    def set_senha(self, senha):
        self._senha = senha

    def to_dict(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "matricula": self.matricula,
            "alias": self.alias,
            "id": self.id,
        }
    

    def to_Model(self, data: dict):
        novo_model = UserModel()
        novo_model.nome = data.get("nome", "")
        novo_model.email = data.get("email", "")
        novo_model.matricula = data.get("matricula", "")
        novo_model.alias = data.get("alias", "")
        novo_model.id = data.get("id", "")
        novo_model.set_senha(data.get("senha", ""))
        
        return novo_model