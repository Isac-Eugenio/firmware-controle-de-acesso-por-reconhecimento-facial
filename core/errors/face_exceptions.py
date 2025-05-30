class FaceRecognitionException(Exception):
    def __init__(self, message, details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        return self.message

class FaceEncodingError(FaceRecognitionException):
    def __init__(self, message, details=None):
        full_message = f"Encoding exception: {message}"
        super().__init__(full_message, details)


class FaceLocationError(FaceRecognitionException):
    def __init__(self, message="Face location exception", details=None):
        full_message = f"Location exception: {message}"
        super().__init__(full_message, details)


class FaceMatchError(FaceRecognitionException):
    def __init__(self, message="Recognition exception", details=None):
        full_message = f"Recognition exception: {message}"
        super().__init__(full_message, details)

class FaceModelError(FaceRecognitionException):
    def __init__(self, message, details=None):
        full_message = f"Face Model exception: {message}"
        super().__init__(full_message, details)
