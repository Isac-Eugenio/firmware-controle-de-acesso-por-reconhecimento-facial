# Base: herda da Exception padrão do Python
class CameraException(Exception):
    def __init__(self, message):
        super().__init__(f"Camera Exception: {message}")

# Erro de valor inválido (ex: tamanho ou tipo errado)
class CameraValueError(CameraException):
    def __init__(self, message):
        super().__init__(f"Camera Value Error: {message}")

# Outro exemplo: erro de conexão
class CameraConnectionError(CameraException):
    def __init__(self, message):
        super().__init__(f"Camera Connection Error: {message}")

# Outro exemplo: erro de autenticação
class CameraAuthError(CameraException):
    def __init__(self, message):
        super().__init__(f"Camera Auth Error: {message}")
