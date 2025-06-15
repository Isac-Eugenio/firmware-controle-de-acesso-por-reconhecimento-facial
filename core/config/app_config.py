from dataclasses import dataclass, field
from typing import List, Literal
import yaml


# Carrega configurações do YAML
def load_config(path="core/config/config.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


config = load_config()

# Tipos fixos (substituindo Enum)
CameraFormat = Literal["jpg", "bmp", "mjpeg"]
CameraResolution = Literal[
    "96x96",
    "160x120",
    "176x144",
    "240x176",
    "240x240",
    "320x240",
    "400x296",
    "480x320",
    "640x480",
    "800x600",
    "1024x768",
    "1280x720",
    "1280x1024",
    "1600x1200",
]


@dataclass
class CameraConfig:
    host: str = config["hosts"]["camera"]
    port: int = config["ports"]["camera"]
    resolution: CameraResolution = "800x600"
    format: CameraFormat = "jpg"

    @property
    def custom_host(self) -> str:
        return f"http://{self.host}:{self.port}/{self.resolution}.{self.format}"


@dataclass
class DatabaseConfig:
    host: str = config["hosts"]["database"]
    port: int = config["ports"]["database"]
    user: str = config["credentials"]["database"]["user"]
    password: str = config["credentials"]["database"]["password"]
    name: str = config["credentials"]["database"]["name"]


@dataclass
class DatabaseTables:
    perfis: str = config["details"]["database"]["tables"]["perfis"]["name"]
    dispositivos: str = config["details"]["database"]["tables"]["dispositivos"]
    historico: str = config["details"]["database"]["tables"]["historico"]


from dataclasses import dataclass, field
from typing import List


@dataclass
class PerfisColumns:
    public: List[str] = field(
        default_factory=lambda: config["details"]["database"]["tables"]["perfis"][
            "columns"
        ]["others"]
    )
    private: List[str] = field(
        default_factory=lambda: config["details"]["database"]["tables"]["perfis"][
            "columns"
        ]["others"]
        + [config["details"]["database"]["tables"]["perfis"]["columns"]["password"]]
    )
    encoding: str = field(
        default_factory=lambda: config["details"]["database"]["tables"]["perfis"][
            "columns"
        ]["encoding"]
    )

    password: str = field(
        default_factory=lambda: config["details"]["database"]["tables"]["perfis"][
            "columns"
        ]["password"]
    )

    @property
    def full_columns(self) -> List[str]:
        return self.private + [self.encoding]
    
    