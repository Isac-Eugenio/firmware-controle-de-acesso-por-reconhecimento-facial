class ApiException(Exception):
    def __init__(self, message, details=None):
        self.message = message 
        self.details = details
        super().__init__(message)

    def __str__(self):
        return self.message
    
class ApiDatabaseError(ApiException):
    def __init__(self, message, details=None):
        full_message = f"ApiDatabase Exception: {message}"
        super().__init__(full_message, details)
        self.message = message
