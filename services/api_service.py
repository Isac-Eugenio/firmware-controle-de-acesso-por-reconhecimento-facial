import random
from core.Camera import Camera
from core.exceptions.face_exceptions import FaceServiceError
from models.face_model import FaceUtils
from .database_service import DatabaseService
from core.config.config import config
import numpy as np
import ast

_COLUMNS_DATABASE_PERFIS = config["details"]["database"]["tables"]["perfis"]["columns"]
_PASSWORD_COLUMN = config["details"]["database"]["tables"]["perfis"]["password_column"]
_ENCODING_COLUMN = config["details"]["database"]["tables"]["perfis"]["encoding_column"]
_NAME_TABLE_PERFIS = config["details"]["database"]["tables"]["perfis"]["name"]

_TRUST = config["details"]["database"]["tables"]["perfis"]["trust"]

_HOST_CAMERA = config["hosts"]["camera"]
_PORT_CAMERA = config["ports"]["camera"]
_CONFIG_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CONFIG_CAMERA_FORMAT = config["details"]["camera"]["format"]

class ApiService:
    def __init__(self):
        try:
            _camera = Camera(_HOST_CAMERA, _PORT_CAMERA)
            _frame = _camera.get_frame(_CONFIG_CAMERA_RESOLUTION, _CONFIG_CAMERA_FORMAT)

            self.fr = FaceUtils(_frame)
            self.db = DatabaseService()
            self._camera = _camera

        except Exception as e:
            raise FaceServiceError("Erro ao inicializar o FaceService", str(e))

    def _update_camera(self):
        """Método para atualizar o frame da câmera e atualizar o FaceUtils."""
        try:
            _frame = self._camera.get_frame(_CONFIG_CAMERA_RESOLUTION, _CONFIG_CAMERA_FORMAT)
            self.fr.update_frame(_frame)
            
        except Exception as e:
            raise FaceServiceError("Erro ao atualizar a câmera", str(e))

    def _generate_id(self):
        return str(random.randint(0, 99999999)).zfill(8)
    
    def _ensure_str_values(self, data: dict):
        return {key: f"'{value}'" for key, value in data.items()}
    
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



    async def _insert_user(self, data: dict):
        yield {"id": "01", "message": "Coletando dados do formulário!", "status": True, "final": False}
        data_admin = data.get('admin_data')
        data_user = data.get('user_data')

        # TRY 1: Verificação de autorização
        try:
            yield {"id": "02", "message": "Verificando autorização!", "status": False, "final": False}

            if data_admin is None:
                yield {"id": "02", "message": "Usuário não autorizado!", "status": False, "final": True}
                return

            if data_user is None:
                yield {"id": "02", "message": "Sem dados do novo perfil!", "status": False, "final": True}
                return

            # Mantida conforme solicitado
            condition = " AND ".join([f"{key} = '{value}'" for key, value in dict(data_admin).items()])

            admin_check = await self.db.count(
                table="usuarios",
                condition=condition
            )

            admin_check = admin_check['result']['result']

            print(admin_check)
            if not bool(admin_check):
                yield {"id": "02", "message": "Usuário não autorizado para criar novos usuários!", "status": False, "final": True}
                return

        except Exception as e:
            yield {"id": "02", "message": f"Erro na autorização: {str(e)}", "status": False, "final": True}
            return

        # ID do novo perfil
        yield {"id": "03", "message": "Gerando ID do novo perfil!", "status": True, "final": False}
        data = dict(data_user)
        data['id'] = self._generate_id()

        # Etapa 1: Início do cadastro
        yield {"id": "01", "message": "Iniciando cadastro", "status": True, "final": False}

        # TRY 2: Captura facial
        try:
            yield {"id": "02", "message": "Capturando rosto...", "status": True, "final": False}

            face_data = self._extract_valid_face_encoding()

            if not face_data.get("status"):
                yield {"id": "02", "message": "Nenhum rosto detectado", "status": False, "final": True}
                return

            yield {"id": "02", "message": "Rosto capturado", "status": True, "final": False}

        except Exception as e:
            yield {"id": "02", "message": f"Erro ao capturar rosto: {str(e)}", "status": False, "final": True}
            return

        # Etapa 3: Preparando dados
        yield {"id": "03", "message": "Preparando cadastro...", "status": True, "final": False}
        encoding = ",".join(str(x) for x in face_data["encoding"])
        data[_ENCODING_COLUMN] = encoding

        # TRY 3: Envio ao banco de dados
        try:
            yield {"id": "04", "message": "Enviando dados...", "status": True, "final": False}

            await self.db._ensure_connected()

            result = await self.db.insert(table=_NAME_TABLE_PERFIS, data=data)

            if not result.get("status", False):
                yield {"id": "04", "message": "Erro ao cadastar o novo perfil", "status": False, "final": True}
                return
            yield {
                "id": "05",
                "message": "Perfil cadastrado com sucesso",
                "status": True,
                "data": result, 
                "final": True
            }

        except Exception as e:
                print(e)
                yield {"id": "04", "message": "Falha no cadastro", "status": False, "final": True}
                return


    async def _update_user(self, data: dict, encoding_column: str, table: str):
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


    async def _delete_user(self, data: dict, table: str):
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


    async def _search(self, data: dict, table: str):
        return await self._get_data(data=data, table=table)
