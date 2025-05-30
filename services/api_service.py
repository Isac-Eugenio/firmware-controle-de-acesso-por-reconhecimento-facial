import random
from models.camera_model import Camera
from core.errors.face_exceptions import FaceServiceError
from models.face_model import FaceUtils
from repository.database_repository import DatabaseRepository
from core.config.app_config import config
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
            self.db = DatabaseRepository()
            self._camera = _camera

        except Exception as e:
            raise FaceServiceError("Erro ao inicializar o FaceService", str(e))

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
