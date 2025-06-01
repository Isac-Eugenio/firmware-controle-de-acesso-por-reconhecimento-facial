class CameraException(Exception):
    def __init__(self, message, details=None):
        self.details = details
        self.message = message
        super().__init__(message)

    def __str__(self):
        return self.message

class CameraValueError(CameraException):
    def __init__(self, message, details=None):
        full_message = f"CameraValueError: {message}"
        super().__init__(full_message, details)
        self.message = message

class CameraConnectionError(CameraException):
    def __init__(self, message, details=None):
        full_message = f"CameraConnectionError: {message}"
        super().__init__(full_message, details)
        self.message = message

class CameraAuthError(CameraException):
    def __init__(self, message, details=None):
        full_message = f"CameraAuthError: {message}"
        super().__init__(full_message, details)
        self.message = message
