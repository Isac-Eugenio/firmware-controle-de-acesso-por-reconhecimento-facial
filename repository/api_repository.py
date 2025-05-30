import numpy as np
from controllers.camera_controller import CameraController
from core.config.app_config import config
from core.errors.face_exceptions import FaceServiceError


_COLUMNS_DATABASE_PERFIS = config["details"]["database"]["tables"]["perfis"]["columns"]
_PASSWORD_COLUMN = config["details"]["database"]["tables"]["perfis"]["password_column"]
_ENCODING_COLUMN = config["details"]["database"]["tables"]["perfis"]["encoding_column"]
_NAME_TABLE_PERFIS = config["details"]["database"]["tables"]["perfis"]["name"]

_TRUST = config["details"]["database"]["tables"]["perfis"]["trust"]

_HOST_CAMERA = config["hosts"]["camera"]
_PORT_CAMERA = config["ports"]["camera"]
_CONFIG_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CONFIG_CAMERA_FORMAT = config["details"]["camera"]["format"]

class ApiRepository:
    def __init__(self):
        self.camera_controller = CameraController()
        self._update_camera = self.camera_controller._update_camera()

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


    async def _get_table(self, columns:list = None, table:str=None):
        if not columns is None: 
            get = await self.db.select(columns=columns, table=table)
            return get
        else:
            get = await self.db.select(table=table)
            return get
        
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
    
    async def _verify_user(self, data: dict):
        try:
            await self.db._ensure_connected()

            condition = " AND ".join([f"{key} = '{value}'" for key, value in data.items()])
            result = await self.db.count(table=_ENCODING_COLUMN, condition=condition)
            
            return result
        
        except Exception as e:
            raise FaceServiceError("Erro ao verificar usuário", str(e))
 
    async def _validate_user(self):
        
        columns = _COLUMNS_DATABASE_PERFIS.append(_ENCODING_COLUMN)

        try:
            # Etapa 1: Inicialização da câmera
            try:
                self._update_camera()
                yield {"id": "01", "message": "Cam starting", "status": True, "final": False}
                if not self._camera.status():
                    yield {"id": "01", "message": "Cam off", "status": False, "final": True}
                    return
                
                yield {"id": "01", "message": "Cam OK", "status": False, "final": True}

            except Exception as e:
                yield {"id": "01", "message": "Erro Cam", "status": False, "final": True}

            result = self.fr.encodings()
            face_encodings = result["encodings"]

            if not face_encodings:
                yield {"id": "02", "message": "Sem rosto", "status": False, "final": True}
                return
            
            yield {"id": "02", "message": "Rosto lido", "status": True, "final": False}

            # Etapa 3: Verificação
            await self.db._ensure_connected()
            db_result = await self.db.select(table=_NAME_TABLE_PERFIS, columns=columns)
            if not db_result["status"] or not db_result["result"]:
                yield {"id": "03", "message": "Acesso negado", "status": False, "final": True}
                return
            yield {"id": "03", "message": "Verificando...", "status": True, "final": False}

            # Etapa 4: Comparação facial
            best_match = None
            best_distance = float('inf')

            for user in db_result["result"]:
                db_encoding_str = getattr(user, _ENCODING_COLUMN, None)
                print(f"DB string: {db_encoding_str}")

                if not db_encoding_str:
                    continue

                # Se os valores no encoding estiverem separados por vírgulas
                db_encoding = np.array([float(x) for x in db_encoding_str.split(',')])

                print(f"DB Encoding (np.array): {db_encoding}")
                print(f"Face Encoding: {face_enc}")
                for face_enc in face_encodings:
                    is_match = self.fr.compare_faces(face_encoding_to_check=face_enc, known_face_encodings=[db_encoding], trust=_TRUST)[0]

                    if is_match:
                        distance = np.linalg.norm(db_encoding - face_enc)
                        if distance < best_distance:
                            best_distance = distance
                            best_match = user

            if best_match:
                best_match = dict(best_match)
                best_match.pop(_ENCODING_COLUMN, None)
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
