from repository.database_repository import DatabaseRepository


class ApiController:
    def __init__(self, database_repository: DatabaseRepository):
        self.database_repository = database_repository
    
    