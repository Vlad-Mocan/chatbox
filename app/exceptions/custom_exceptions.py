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
