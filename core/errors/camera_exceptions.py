# Base: exceção geral de câmera
class CameraException(Exception):
    def __init__(self, message, details=None):
        self.details = details
        super().__init__(message)

# Exceção para erros de valor (ex: resolução inválida, formato incorreto etc.)
class CameraValueError(CameraException):
    def __init__(self, message, details=None):
        full_message = f"Camera valueError: {message}"
        super().__init__(message, details)

# Exceção para falha de conexão com a câmera
class CameraConnectionError(CameraException):
    def __init__(self, message, details=None):
        full_message = f"Camera connectionError: {message}"
        super().__init__(message, details)

# Exceção para erro de autenticação (ex: token inválido, permissão negada etc.)
class CameraAuthError(CameraException):
    def __init__(self, message, details=None):
        full_message = f"Camera authError {message}"
        super().__init__(message, details)
