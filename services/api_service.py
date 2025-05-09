from db.Database import Database
import datetime
import random 

class ApiService:
    def __init__(self):
        self.database = Database()
        pass

    def generate_id():
        timestamp = datetime.now().strftime('%d%m%H%M%S')  # ex: 0905123059
        random_number = random.randint(10, 99)
        return timestamp + str(random_number)
    
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
            condition = " AND ".join([f"{key} = :{key}" for key in data_admin.keys()])
            
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

