import voyageai
from app.core.config import settings

voyage_client = voyageai.Client(api_key=settings.voyage_api_key)
