from pydantic import BaseModel
from datetime import datetime


class FileResponse(BaseModel):
    id: int
    original_name: str
    content_type: str
    size: int
    created_at: datetime

    model_config = {"from_attributes": True}


class SearchResultResponse(BaseModel):
    rank: float
    file: FileResponse


class SemanticSearchResultResponse(BaseModel):
    similarity: float
    file: FileResponse
