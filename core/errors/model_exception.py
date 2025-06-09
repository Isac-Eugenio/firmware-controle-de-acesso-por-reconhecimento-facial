class ModelException(Exception):
    def __init__(self, message, details=None):
        self.message = message 
        self.details = details
        super().__init__(message)

    def __str__(self):
        return self.message

class ModelValueError(ModelException):
    def __init__(self, message, details=None, cls_name: str = None):
        if cls_name:
            full_message = f"Model ValueError [{cls_name}]: {message}"
        else:
            full_message = f"Model ValueError: {message}"
        super().__init__(full_message, details)
        self.message = message


class ModelAttributeError(ModelException):
    def __init__(self, message, details=None, cls_name: str = None):
        if cls_name:
            full_message = f"Model AttributeError [{cls_name}]: {message}"
        else:
            full_message = f"Model AttributeErro: {message}"
        super().__init__(full_message, details)
        self.message = message