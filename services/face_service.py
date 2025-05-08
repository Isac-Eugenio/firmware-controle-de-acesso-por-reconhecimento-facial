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

            # pega só o vetor de encodings
            encodings = result.get("encodings", [])

            # valida se veio ao menos um
            if not encodings:
                raise FaceServiceError("Nenhum rosto detectado", result)

            # retorna o primeiro encoding convertido para lista
            return {"status": True, "encoding": encodings[0].tolist()}

        except FaceServiceError:
            # reaproveita erros intencionais
            raise
        except Exception as e:
            # outros erros
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

    async def _validate_user(self, columns: list, table: str, encoding_column: str, trust: int):
        columns.append(encoding_column)

        try:
            # Etapa 1: Inicialização da câmera
            self._update_camera()
            yield {"id": "01", "message": "Cam iniciada", "status": True, "final": False, "start": True}

            # Etapa 2: Captura facial
            result = self.fr.encodings()
            face_encodings = result["encodings"]
            if not face_encodings:
                yield {"id": "02", "message": "Sem rosto", "status": False, "final": True}
                return
            yield {"id": "02", "message": "Rosto lido", "status": True, "final": False}

            # Etapa 3: Verificação
            await self.db._ensure_connected()
            db_result = await self.db.select(table=table, columns=columns)
            if not db_result["status"] or not db_result["result"]:
                yield {"id": "03", "message": "Acesso negado", "status": False, "final": True}
                return
            yield {"id": "03", "message": "Verificando...", "status": True, "final": False}

            # Etapa 4: Comparação facial
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
                best_match = dict(best_match)
                best_match.pop(encoding_column, None)
                yield {
                    "id": "04",
                    "message": f"Ola! {best_match['alias']}",
                    "status": True,
                    "data": best_match,
                    "final": True
                }
            else:
                yield {
                    "id": "04",
                    "message": "Acesso negado",
                    "status": False,
                    "data": None,
                    "final": True
                }

        except Exception as e:
            yield {
                "id": "05",
                "message": "Erro ao ler",
                "status": False,
                "data": str(e),
                "final": True
            }



    async def insert_user(self, data: dict, encoding_column: str, table: str):
        try:
            # Etapa 1: início do cadastro
            yield {"id": "01", "message": "Iniciando cadastro", "status": True, "final": False}

            # Etapa 2: captura facial
            yield {"id": "02", "message": "Capturando rosto...", "status": True, "final": False}
            face_data = self._extract_valid_face_encoding()

            if not face_data["status"]:
                yield {"id": "02", "message": "Nenhum rosto detectado", "status": False, "final": True}
                return
            yield {"id": "02", "message": "Rosto capturado", "status": True, "final": False}

            # Etapa 3: preparando dados
            yield {"id": "03", "message": "Preparando cadastro...", "status": True, "final": False}
            encoding = ",".join(str(x) for x in face_data["encoding"])

            data[encoding_column] = encoding

            # Etapa 4: envio ao servidor
            yield {"id": "04", "message": "Enviando dados...", "status": True, "final": False}

            await self.db._ensure_connected()
            
            result = await self.db.insert(table=table, data=data)

            if not result["status"]:
                yield {"id": "04", "message": "Falha no cadastro", "status": False, "final": True}
                return

            # Etapa 5: sucesso
            yield {
                "id": "05",
                "message": "Usuário cadastrado com sucesso",
                "status": True,
                "data": result,
                "final": True
            }

        except Exception as e:
            yield {
                "id": "06",
                "message": "Erro no cadastro",
                "status": False,
                "data": str(e),
                "final": True
            }

    
    async def update_user(self, data: dict, encoding_column: str, table: str):
        try:
            # Etapa 1: iniciar câmera
            yield {"id": "01", "message": "Iniciando câmera", "status": True, "final": False}

            # Etapa 2: capturar rosto
            yield {"id": "02", "message": "Capturando rosto...", "status": True, "final": False}
            face_data = self._extract_valid_face_encoding()
            if not face_data["status"]:
                yield {"id": "02", "message": "Nenhum rosto", "status": False, "final": True}
                return
            yield {"id": "02", "message": "Rosto capturado", "status": True, "final": False}

            # Etapa 3: preparar dados
            yield {"id": "03", "message": "Preparando...", "status": True, "final": False}
            encoding = ",".join(str(x) for x in face_data["encoding"])
            data[encoding_column] = encoding
            condition = " AND ".join([f"{k} = '{v}'" for k, v in data.items()])

            # Etapa 4: atualizar usuário
            yield {"id": "04", "message": "Atualizando...", "status": True, "final": False}
            await self.db._ensure_connected()
            result = await self.db.update(table=table, data=data, condition=condition)

            if not result["status"]:
                yield {"id": "04", "message": "Falha atualização", "status": False, "final": True}
                return

            if not result["result"]:
                yield {"id": "04", "message": "Nada alterado", "status": False, "final": True}
                return

            # Etapa 5: sucesso
            yield {
                "id": "05",
                "message": "Atualização concluída",
                "status": True,
                "data": result,
                "final": True
            }

        except Exception as e:
            yield {
                "id": "06",
                "message": "Erro ao atualizar",
                "status": False,
                "data": str(e),
                "final": True
            }


    async def delete_user(self, data: dict, table: str):
        try:
            # Etapa 1: iniciar exclusão
            yield {"id": "01", "message": "Iniciando...", "status": True, "final": False}

            # Etapa 2: excluir usuário
            yield {"id": "02", "message": "Excluindo...", "status": True, "final": False}
            await self.db._ensure_connected()
            result = await self.db.delete(table=table, data=data)

            if not result["status"]:
                yield {"id": "02", "message": "Falha exclusão", "status": False, "final": True}
                return

            if not result["result"]:
                yield {"id": "02", "message": "Nada excluído", "status": False, "final": True}
                return

            # Etapa 3: sucesso
            yield {
                "id": "03",
                "message": "Exclusão concluída",
                "status": True,
                "data": result,
                "final": True
            }

        except Exception as e:
            yield {
                "id": "04",
                "message": "Erro ao excluir",
                "status": False,
                "data": str(e),
                "final": True
            }


    async def search(self, data: dict, table: str):
        return await self._get_data(data=data, table=table)
