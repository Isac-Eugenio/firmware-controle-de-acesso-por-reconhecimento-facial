from repository.database_repository import DatabaseRepository
from services.face_service import FaceService


class ApiService:
    def __init__ (self, face_service : FaceService, database_repository: DatabaseRepository):
        self.face_service = face_service
        self.db_repository = database_repository
        