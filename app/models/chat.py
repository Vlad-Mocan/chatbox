from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    limit: int = 5


class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
