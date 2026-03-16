from fastapi import FastAPI
from app.core.lifespan import lifespan
from app.api.routes.core import router as core_router
from app.api.routes.auth import router as auth_router
from app.exceptions.handlers import register_exception_handlers
import uvicorn

app = FastAPI(lifespan=lifespan)

app.include_router(core_router, tags=["Core"])
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

register_exception_handlers(app)

def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()