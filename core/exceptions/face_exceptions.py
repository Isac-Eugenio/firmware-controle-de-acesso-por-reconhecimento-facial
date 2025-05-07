
class FaceServiceError(Exception):
    def __init__(self, message, data=None):
        self.message = message
        self.data = data
        super().__init__(self.message)


class FaceRecognitionError(Exception):
    def __init__(self, message, details=None):
        self.message = message
        self.details = details
        super().__init__(self.message)
