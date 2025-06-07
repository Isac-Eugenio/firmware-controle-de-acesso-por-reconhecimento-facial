import yaml
from enum import Enum

def load_config(path="config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()

# Enums para nomes das tabelas
class DatabaseTables(Enum):
    PERFIS = config["details"]["database"]["tables"]["perfis"]["name"]
    HISTORICO = config["details"]["database"]["tables"]["historico"]["name"]
    DEVICES = config["details"]["database"]["tables"]["devices"]["name"]

# Enum para colunas importantes na tabela 'perfis'
class PerfisColumns(Enum):
    PASSWORD = config["details"]["database"]["tables"]["perfis"]["password_column"]
    ENCODING = config["details"]["database"]["tables"]["perfis"]["encoding_column"]
    PRIVATE = config["details"]["database"]["tables"]["perfis"]["columns"]
    PUBLIC = config["alias"]["columns_for_model"]
    
# Enum para camera formatos (se quiser forçar as opções possíveis)
class CameraFormat(Enum):
    JPG = "JPG"
    PNG = "PNG"
    BMP = "BMP"

# Enum para camera resoluções (exemplo)
class CameraResolution(Enum):
    RES_800x600 = "800x600"
    RES_1024x768 = "1024x768"
    RES_1280x720 = "1280x720"

# Constantes normais
_HOST_CAMERA = config["hosts"]["camera"]
_HOST_DATABASE = config["hosts"]["database"]

_PORT_CAMERA = config["ports"]["camera"]
_PORT_DATABASE = config["ports"]["database"]

_DATABASE_USER = config["credentials"]["database"]["user"]
_DATABASE_PASSWORD = config["credentials"]["database"]["password"]
_DATABASE_NAME = config["credentials"]["database"]["name"]

_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CAMERA_FORMAT = config["details"]["camera"]["format"]

_TABLE_PERFIS_TRUST = config["details"]["database"]["tables"]["perfis"]["trust"]
