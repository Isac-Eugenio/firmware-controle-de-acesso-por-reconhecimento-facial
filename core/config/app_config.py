import yaml
from enum import Enum

def load_config(path="core/config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()

# Enums opcionais (caso queira manter validações)
class CameraFormat(Enum):
    JPG = "JPG"
    PNG = "PNG"
    BMP = "BMP"

class CameraResolution(Enum):
    RES_800x600 = "800x600"
    RES_1024x768 = "1024x768"
    RES_1280x720 = "1280x720"

# Constantes de configuração
_HOST_CAMERA = config["hosts"]["camera"]
_HOST_DATABASE = config["hosts"]["database"]

_PORT_CAMERA = config["ports"]["camera"]
_PORT_DATABASE = config["ports"]["database"]

_DATABASE_USER = config["credentials"]["database"]["user"]
_DATABASE_PASSWORD = config["credentials"]["database"]["password"]
_DATABASE_NAME = config["credentials"]["database"]["name"]

_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CAMERA_FORMAT = config["details"]["camera"]["format"]
