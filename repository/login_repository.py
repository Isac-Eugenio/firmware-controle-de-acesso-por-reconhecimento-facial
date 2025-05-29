from .database_repository import DatabaseRepository

class LoginRepository:
    def __init__(self, form: dict):
        self.database = DatabaseRepository()
        self._form = form

    async def login(self):
        try:
            condition = "email = :email AND senha = :senha AND permission_level = :permission_level"
            values = {
                "email": self._form["email"],
                "senha": self._form["senha"],
                "permission_level": "adminstrador"
            }

            result = await self.database.select(
                columns=["email", "alias", "permission_level", "id", "matricula"],
                condition=condition,
                table="usuarios",
                values=values
            )

            if result['status'] and result['result']:
                data = dict(result['result'][0])
                return {'auth': True, 'dados': dict(result['result'][0]), 'error': None}
            
            else:
                return {'auth': False, 'dados': {}, 'error': None}

        except Exception as e:
            print(str(e))
            return {'auth': False, 'dados': {}, 'error': "Erro ao autenticar o usuário"}

    