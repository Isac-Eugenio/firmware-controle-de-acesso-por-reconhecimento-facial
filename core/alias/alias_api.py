from core.config.app_config import config


# ALIAS DATABASE

_ENCODING_COLUMN = _ENCODING_COLUMN = config["details"]["database"]["tables"]["perfis"][
    "encoding_column"
]
_PRIVATE_COLUMNS_PERFIS = config["details"]["database"]["tables"]["perfis"]["columns"]
_NAME_TABLE_PERFIS = config["details"]["database"]["tables"]["perfis"]["name"]
_PUBLIC_COLUMNS_PERFIS = config["alias"]["columns_for_model"]
_PASSWORD_COLUMN = config["details"]["database"]["tables"]["perfis"]["password_column"]
# ALIAS PARA CAMERA

_HOST_CAMERA = config["hosts"]["camera"]
_PORT_CAMERA = config["ports"]["camera"]
_CONFIG_CAMERA_RESOLUTION = config["details"]["camera"]["resolution"]
_CONFIG_CAMERA_FORMAT = config["details"]["camera"]["format"]
