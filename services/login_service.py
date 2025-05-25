from services.database_service import DatabaseService

class LoginService:
    def __init__(self, form: dict):
        self.database = DatabaseService()
        self._form = form

    async def login(self):
        try:
            condition = "email = :email AND senha = :senha"
            values = {
                "email": self._form["email"],
                "senha": self._form["senha"]
            }

            result = await self.database.select(
                columns=["email", "alias", "permission_level", "id"],
                condition=condition,
                table="usuarios",
                values=values
            )
            if result['status'] and result['result']:
                data = dict(result['result'][0])
                if data['permission_level'] == 'adminstradorstrador':
                    return {'permission_level': True, 'dados': dict(result['result'][0]), 'error': None}
                else:
                    return {'permission_level': False, 'dados': {}, 'error': None}
            else:
                return {'permission_level': False, 'dados': {}, 'error': None}

        except Exception as e:
            return {'permission_level': False, 'dados': {}, 'error': str(e)}

    