from sqlalchemy.orm import Session
from groq import Groq

from app.core.config import settings
from app.repositories.file_repository import FileRepository
from app.core.voyage_client import voyage_client

groq_client = Groq(api_key=settings.groq_api_key)


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.file_repo = FileRepository(db)

    def chat(self, query: str, limit: int, current_user_id: int) -> dict:
        limit = max(1, min(limit, 20))

        response = voyage_client.embed(query, model="voyage-3", output_dimension=1024)
        embedding = response.embeddings[0]

        chunks = self.file_repo.get_chunks_for_rag(embedding, limit, current_user_id)

        if not chunks:
            return {
                "answer": "I couldn't find any relevant content in your files to answer that question.",
                "sources": [],
            }

        context_parts = []
        for chunk in chunks:
            context_parts.append(f"[Source: {chunk['file_name']}]\n{chunk['text']}")
        context = "\n\n---\n\n".join(context_parts)

        sources = list(dict.fromkeys(chunk["file_name"] for chunk in chunks))

        completion = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. Answer the user's question using only "
                        "the provided context from their files. If the context does not contain "
                        "enough information to answer, say so clearly. Do not make up information."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion: {query}",
                },
            ],
        )

        answer = completion.choices[0].message.content

        return {"answer": answer, "sources": sources}
