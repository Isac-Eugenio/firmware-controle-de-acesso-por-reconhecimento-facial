from db.Database import Database
import random 

class ApiService:
    def __init__(self):
        self.database = Database()
        pass

    def _generate_id(self):
         return str(random.randint(0, 99999999)).zfill(8)
    
    def _ensure_str_values(self, data: dict):
        return {key: f"'{value}'" for key, value in data.items()}

    async def get_table(self, columns:list = None, table:str=None):
        if not columns is None: 
            get = await self.database.select(columns=columns, table=table)
            return get
        else:
            get = await self.database.select(table=table)
            return get
    
    async def insert_user_api(self, form: dict):
        data_admin = form.get('admin_data')  # Obtendo os dados do admin
        user_admin = form.get('user_data')   # Obtendo os dados do novo usuário

        user_admin = dict(user_admin)
        user_admin['id'] = self._generate_id()
        
        # Garantindo que todos os valores em user_admin sejam strings
       # user_admin = self._ensure_str_values(user_admin)

        try:
            # Verificando se os dados do admin estão presentes
            if data_admin is None:
                raise Exception("Usuário sem autorização de acesso!")
            
            # Verificando se os dados do novo usuário estão presentes
            if user_admin is None:
                raise Exception("Sem dados do novo usuário!")
            
            # Construindo a condição WHERE dinamicamente com base nas chaves e valores do admin_data
            condition = " AND ".join([f"{key} = '{value}'" for key, value in dict(data_admin).items()])
            print(f"SELECT COUNT(*) FROM usuarios WHERE {condition}")
            
            # Verificando se o admin existe no banco de dados
            admin_check = await self.database.count(
                table="usuarios", 
                condition=condition
            )
            
            # Se o admin não for encontrado, retornar erro
            if not bool(admin_check):
                raise Exception("Usuário não autorizado para criar novos usuários!")

            # Adicionando o novo usuário ao banco de dados
            insert_result = await self.database.insert(
                table="usuarios",
                data=user_admin  # Passando os dados diretamente
            )
            
            # Se a inserção foi bem-sucedida, retorna True
            if insert_result:
                return dict(insert_result)
            else:
                raise Exception("Erro ao inserir novo usuário!")
        
        except Exception as e:
            # Retorna o erro se algo deu errado
            return str(e)


