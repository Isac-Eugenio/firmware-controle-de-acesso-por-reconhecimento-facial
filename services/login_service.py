from db.Database import Database

class LoginService:
    def __init__(self, form: dict):
        self.database = Database()
        self._form = form

    async def login(self):
        try:
            condition = "email = :email AND senha = :senha"
            values = {
                "email": self._form["email"],
                "senha": self._form["senha"]
            }

            result = await self.database.select(
                columns=["email", "nome", "auth"],
                condition=condition,
                table="usuarios",
                values=values
            )

            if result['status'] and result['result']:
                data = dict(result['result'][0])
                if data['auth'] == 'docente':
                    return {'auth': True, 'dados': dict(result['result'][0]), 'error': None}
                else:
                    return {'auth': False, 'dados': {}, 'error': None}
            else:
                return {'auth': False, 'dados': {}, 'error': None}

        except Exception as e:
            return {'auth': False, 'dados': {}, 'error': str(e)}

    