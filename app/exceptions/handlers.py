from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.exceptions.custom_exceptions import EmailAlreadyExistsException, InvalidCredentialsException, InvalidAuthorizationException, UserNotFoundException


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(EmailAlreadyExistsException)
    async def email_already_exists_handler(_request: Request, exc: EmailAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content={"detail": f"Email '{exc.email}' is already registered"},
        )

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(_request: Request, exc: InvalidCredentialsException):
        return JSONResponse(
            status_code=401,
            content={"detail": "The credentials you have submitted are incorrect."},
        )

    @app.exception_handler(InvalidAuthorizationException)
    async def invalid_authorization_handler(_request: Request, exc: InvalidAuthorizationException):
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid or missing authorization token."},
        )

    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(_request: Request, exc: UserNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"detail": "User not found."},
        )
