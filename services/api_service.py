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
    