from core.Camera import Camera 
from core.FaceUtils import FaceUtils
from db.Database import Database
from core.config import config
import numpy as np

class FaceService:
    def __init__(self):
        _camera = Camera(config["hosts"]["camera"], config["ports"]["camera"])
        _frame = _camera.get_frame(config["details"]["camera"]["resolution"], 
                                   config["details"]["camera"]["format"])
        
        self.fr = FaceUtils(_frame)
        self.db = Database()
        self._camera = _camera

    def _update_camera(self):
        """Método para atualizar o frame da câmera e atualizar o FaceUtils."""
        _frame = self._camera.get_frame(config["details"]["camera"]["resolution"], 
                                        config["details"]["camera"]["format"])
        self.fr.update_frame(_frame) 

    def _extract_valid_face_encoding(self):

        self._update_camera()

        result = self.fr.encodings()
        print(result)

        if not result["status"]:
            return result

        encodings = result["encodings"]

        return {"status": True, "encoding": encodings[0].tolist()}
     
    async def _get_data(self, data: dict, table: str):

        await self.db._ensure_connected()
        result = await self.db.select(table=table, data=data)

        if not result["status"]:
            return {"status": False, "message": "Erro ao consultar o banco de dados", "data": None}

        if not result["result"]:
            return {"status": False, "message": "Nenhum dado encontrado", "data": None}

        return {"status": True, "message": "Dados encontrados com sucesso", "data": result["result"]}
    
    async def _validate_user(self, data: dict, table: str, encoding_column: str, trust: int):
        # Atualizar a câmera e obter os encodings da face
        self._update_camera()
        result = self.fr.encodings()

        if not result["status"]:
            return result
        
        encodings = result["encodings"]
        encodings = np.array(eval(encodings))  # Converte para np.array para comparação
        
        # Garantir que o banco de dados esteja conectado
        await self.db._ensure_connected()

        # Consulta inicial no banco de dados
        db_result = await self.db.select(table=table, data=data)
        
        if not db_result["status"]:
            return {"status": False, "message": "Erro ao consultar o banco de dados", "data": None}

        if not db_result["result"]:
            return {"status": False, "message": "Nenhum dado encontrado", "data": None}

        # Iterar sobre os resultados do banco de dados
        for user in db_result["result"]:
            # Obter o encoding do banco de dados para comparação
            db_encoding = user.get(encoding_column)
            
            # Verifique se o encoding do banco de dados é válido
            if db_encoding:
                db_encoding = np.array(eval(db_encoding))  # Converte o encoding armazenado para np.array
                
                # Comparar os encodings da face com o encoding do banco de dados
                results = self.fr.compare_faces([db_encoding], encodings)
                
                if results[0]:  # Se encontrar uma correspondência
                    return {"status": True, "message": "Usuário encontrado", "data": user}

        # Caso nenhum usuário tenha correspondido, retornar False
        return {"status": False, "message": "Nenhum usuário correspondente encontrado", "data": None}



    async def insert_user(self, data: dict, encoding_column: str, table: str):

        face_data = self._extract_valid_face_encoding()

        if not face_data["status"]:
            return face_data

        data[encoding_column] = str(face_data["encoding"])

        await self.db._ensure_connected()
        result = await self.db.insert(table=table, data=data)

        return {
            "status": result["status"],
            "message": "Usuário cadastro com sucesso" if result["status"] else "Erro ao cadastrar usuario",
            "data": result
        }
    
    async def update_user(self, data: dict, encoding_column: str, table: str):
        encoding = self._extract_valid_face_encoding()

        if not encoding["status"]:
            return encoding
        
        data[encoding_column] = str(encoding["encoding"])

        await self.db._ensure_connected()

        result = await self.db.update(table=table, data=data)
        if not result["status"]:
            return {"status": False, "message": "Erro ao atualizar o banco de dados", "data": None}
        
        if not result["result"]:
            return {"status": False, "message": "Nenhum dado encontrado", "data": None}
        
        return {
            "status": result["status"],
            "message": "Usuário atualizado com sucesso" if result["status"] else "Erro ao atualizar usuario",
            "data": result
        }
    
    async def delete_user(self, data: dict, table: str):
        await self.db._ensure_connected()
        result = await self.db.delete(table=table, data=data)
        
        if not result["status"]:
            return {"status": False, "message": "Erro ao deletar o banco de dados", "data": None}
        
        if not result["result"]:
            return {"status": False, "message": "Nenhum dado encontrado", "data": None}
        
          
        return {
            "status": result["status"],
            "message": "Usuário deletado com sucesso" if result["status"] else "Erro ao deletar usuario",
            "data": result
        }
    

    async def search(self, data: dict, table : str):
        return await self._get_data(data=data, table=table)
    
