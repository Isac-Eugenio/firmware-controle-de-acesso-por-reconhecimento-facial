from db.Database import Database

class ApiService:
    def __init__(self):
        self.database = Database()
        pass
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
    
    try:
        # Verificando se os dados do admin estão presentes
        if data_admin is None:
            raise Exception("Usuário sem autorização de acesso!")
        
        # Verificando se os dados do novo usuário estão presentes
        if user_admin is None:
            raise Exception("Sem dados do novo usuário!")
        
        # Construindo a condição WHERE dinamicamente com base nas chaves e valores do admin_data
        condition = " AND ".join([f"{key} = '{value}'" for key, value in data_admin.items()])
        
        # Verificando se o admin existe no banco de dados
        admin_check = await self.database.select_one(
            columns=['id'],  # Aqui podemos verificar por qualquer coluna do admin, no caso, apenas 'id'
            table="usuarios", 
            condition=condition
        )
        
        # Se o admin não for encontrado, retornar erro
        if not admin_check:
            raise Exception("Usuário não autorizado para criar novos usuários!")

        # Se o admin for encontrado, então inserir os dados do novo usuário
        columns_user = [key for key in user_admin]
        values_user = [value for value in user_admin]
        
        # Adicionando o novo usuário ao banco de dados
        insert_result = await self.database.insert(
            table="usuarios",
            columns=columns_user,
            values=values_user
        )
        
        # Se a inserção foi bem-sucedida, retorna True
        if insert_result:
            return True
        else:
            raise Exception("Erro ao inserir novo usuário!")
    
    except Exception as e:
        # Retorna o erro se algo deu errado
        return str(e)

