from core.Camera import Camera
from core.exceptions.face_exceptions import FaceServiceError
from core.utils.FaceUtils import FaceUtils
from db.Database import Database
from core.config.config import config
import numpy as np
import ast

class FaceService:
    def __init__(self):
        try:
            _camera = Camera(config["hosts"]["camera"], config["ports"]["camera"])
            _frame = _camera.get_frame(config["details"]["camera"]["resolution"], 
                                       config["details"]["camera"]["format"])

            self.fr = FaceUtils(_frame)
            self.db = Database()
            self._camera = _camera
        except Exception as e:
            raise FaceServiceError("Erro ao inicializar o FaceService", str(e))

    def _update_camera(self):
        """Método para atualizar o frame da câmera e atualizar o FaceUtils."""
        try:
            _frame = self._camera.get_frame(config["details"]["camera"]["resolution"], 
                                            config["details"]["camera"]["format"])
            self.fr.update_frame(_frame)
        except Exception as e:
            raise FaceServiceError("Erro ao atualizar a câmera", str(e))

    def _extract_valid_face_encoding(self):
        try:
            self._update_camera()
            result = self.fr.encodings()

            if not result["status"]:
                raise FaceServiceError("Falha ao obter encodings de face", result)

            encodings = result["encodings"]
            return {"status": True, "encoding": encodings[0].tolist()}

        except Exception as e:
            raise FaceServiceError("Erro ao extrair encoding da face", str(e))
    
    async def _get_data(self, data: dict, table: str):
        try:
            await self.db._ensure_connected()
            result = await self.db.select(table=table, data=data)

            if not result["status"]:
                raise FaceServiceError("Erro ao consultar o banco de dados", result)

            if not result["result"]:
                raise FaceServiceError("Nenhum dado encontrado", result)

            return {"status": True, "message": "Dados encontrados com sucesso", "data": result["result"]}
        
        except Exception as e:
            raise FaceServiceError("Erro ao buscar dados", str(e))
    
    """ 
    TODO: Manutenção

    async def _validate_user(self, data: dict, table: str, encoding_column: str, trust: int):
        try:
            # Atualizar a câmera e obter os encodings da face
            self._update_camera()
            result = self.fr.encodings()

            if not result["status"]:
                raise FaceServiceError("Falha ao obter encodings de face", result)

            encodings = result["encodings"]
            encodings = np.array(eval(encodings))  # Converte para np.array para comparação
            
            # Garantir que o banco de dados esteja conectado
            await self.db._ensure_connected()

            # Consulta inicial no banco de dados
            db_result = await self.db.select(table=table, data=data)
            
            if not db_result["status"]:
                raise FaceServiceError("Erro ao consultar o banco de dados", db_result)

            if not db_result["result"]:
                raise FaceServiceError("Nenhum dado encontrado", db_result)

            # Iterar sobre os resultados do banco de dados
            for user in db_result["result"]:
                db_encoding = user.get(encoding_column)
                if db_encoding:
                    db_encoding = np.array(eval(db_encoding))  # Converte o encoding armazenado para np.array
                    
                    # Comparar os encodings da face com o encoding do banco de dados
                    results = self.fr.compare_faces([db_encoding], encodings, trust=trust)
                    
                    if results[0]:  # Se encontrar uma correspondência
                        return {"status": True, "message": "Usuário encontrado", "data": user}

            raise FaceServiceError("Nenhum usuário correspondente encontrado", None)
        
        except Exception as e:
            raise FaceServiceError("Erro ao validar o usuário", str(e))
 """

    async def _validate_user(self, columns: list, table: str, encoding_column: str, trust: int):
        columns.append(encoding_column)

        try:
            self._update_camera()
            result = self.fr.encodings()

            face_encodings = result["encodings"]  # Certifique-se de acessar os encodings corretamente

            await self.db._ensure_connected()
            db_result = await self.db.select(table=table, columns=columns)

            if not db_result["status"] or not db_result["result"]:
                raise FaceServiceError("Erro ao consultar o banco de dados ou nenhum dado encontrado", db_result)

            best_match = None
            best_distance = float('inf')

            for user in db_result["result"]:
                db_encoding_str = getattr(user, encoding_column, None)
                if not db_encoding_str:
                    continue

                db_encoding = np.array([float(x) for x in db_encoding_str.split(',')])

                for face_enc in face_encodings:
                    is_match = self.fr.compare_faces([db_encoding], face_enc, trust=trust)[0]

                    if is_match:
                        distance = np.linalg.norm(db_encoding - face_enc)
                        if distance < best_distance:
                            best_distance = distance
                            best_match = user

            if best_match:
                best_match = dict(best_match)  # Converte Record em dict
                best_match.pop(encoding_column, None)  # Remove coluna de encoding

                return {
                    "status": True,
                    "message": "Usuário encontrado",
                    "data": best_match
                }

            raise FaceServiceError("Nenhum usuário correspondente encontrado", None)

        except Exception as e:
            raise FaceServiceError("Erro ao validar o usuário", str(e))


    async def insert_user(self, data: dict, encoding_column: str, table: str):
        try:
            face_data = self._extract_valid_face_encoding()

            if not face_data["status"]:
                raise FaceServiceError("Erro ao extrair o encoding da face", face_data)
            encoding = ",".join(str(x) for x in face_data["encoding"])
            data[encoding_column] = encoding
            
            await self.db._ensure_connected()
            result = await self.db.insert(table=table, data=data)

            if not result["status"]:
                raise FaceServiceError("Erro ao cadastrar o usuário", result)

            return {
                "status": result["status"],
                "message": "Usuário cadastrado com sucesso",
                "data": result
            }

        except Exception as e:
            raise FaceServiceError("Erro ao inserir o usuário", str(e))

    
    async def update_user(self, data: dict, encoding_column: str, table: str):
        try:
            encoding = self._extract_valid_face_encoding()

            if not encoding["status"]:
                raise FaceServiceError("Erro ao extrair o encoding da face", encoding)
            
            encoding = ","
            data[encoding_column] = str(encoding["encoding"])

            condition = " AND ".join([f"{key} = '{value}'" for key, value in data.items()])

            await self.db._ensure_connected()
            result = await self.db.update(table=table, data=data, condition=condition)

            if not result["status"]:
                raise FaceServiceError("Erro ao atualizar o banco de dados", result)
            
            if not result["result"]:
                raise FaceServiceError("Nenhum dado encontrado", result)
            
            return {
                "status": result["status"],
                "message": "Usuário atualizado com sucesso" if result["status"] else "Erro ao atualizar usuario",
                "data": result
            }
        
        except Exception as e:
            raise FaceServiceError("Erro ao atualizar o usuário", str(e))
    
    async def delete_user(self, data: dict, table: str):
        try:
            await self.db._ensure_connected()
            result = await self.db.delete(table=table, data=data)

            if not result["status"]:
                raise FaceServiceError("Erro ao deletar o banco de dados", result)
            
            if not result["result"]:
                raise FaceServiceError("Nenhum dado encontrado", result)

            return {
                "status": result["status"],
                "message": "Usuário deletado com sucesso" if result["status"] else "Erro ao deletar usuario",
                "data": result
            }

        except Exception as e:
            raise FaceServiceError("Erro ao deletar o usuário", str(e))

    async def search(self, data: dict, table: str):
        return await self._get_data(data=data, table=table)
