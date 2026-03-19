import uvicorn
from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.api.routes.auth import router as auth_router
from app.api.routes.files import router as files_router
from app.api.routes.chat import router as chat_router
from app.exceptions.handlers import register_exception_handlers

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(files_router, prefix="/files", tags=["Files"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

register_exception_handlers(app)


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
