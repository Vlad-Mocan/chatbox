class EmailAlreadyExistsException(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email already registered: {email}")


class InvalidCredentialsException(Exception):
    def __init__(self):
        super().__init__("The credentials you have submitted are incorrect.")


class InvalidAuthorizationException(Exception):
    def __init__(self):
        super().__init__("Invalid or missing authorization token.")


class UserNotFoundException(Exception):
    def __init__(self):
        super().__init__("User not found.")


class FilenameMissingException(Exception):
    def __init__(self):
        super().__init__("Filename is required.")


class SqlLiteEnvironmentNotSetException(Exception):
    def __init__(self):
        super().__init__("SQL Lite environment variable is not set")


class PostgresEnvironmentNotSetException(Exception):
    def __init__(self):
        super().__init__("PostgreSQL environment variable is not set")


class FileNotFoundException(Exception):
    def __init__(self):
        super().__init__("File cannot be found")
