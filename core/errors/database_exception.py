class DatabaseException(Exception):
    def __init__(self, message, details=None):
        self.message = message       # mensagem "limpa"
        self.details = details
        super().__init__(message)

    def __str__(self):
        return self.message


class DatabaseConnectionError(DatabaseException):
     def __init__(self, message, details=None):
        full_message = f"DatabaseConnection Exception: {message}"
        super().__init__(full_message, details)
        self.message = message

class DatabaseQueryError(DatabaseException):
     def __init__(self, message, details=None):
        full_message = f"DatabaseQuery Exception: {message}"
        super().__init__(full_message, details)
        self.message = message