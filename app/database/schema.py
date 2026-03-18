from app.database.session import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Index,
    Text,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TSVECTOR
from pgvector.sqlalchemy import Vector


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # pylint: disable=not-callable


class FileModel(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    original_name = Column(String, nullable=False)
    random_name = Column(String, nullable=False, index=True)
    content_type = Column(String, nullable=False)
    size = Column(Integer, nullable=False)
    path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # pylint: disable=not-callable


class FileContent(Base):
    __tablename__ = "file_content"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    content_tsv = Column(TSVECTOR, nullable=False)
    embedding = Column(Vector(1024), nullable=True)
    text_content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)

    __table_args__ = (
        Index("idx_file_content_tsv", "content_tsv", postgresql_using="gin"),
        Index(
            "idx_file_content_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 128},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
        Index("idx_file_chunks_file_id", "file_id"),
        Index("idx_file_content_file_id_chunk_seq", "file_id", "chunk_index"),
        UniqueConstraint("file_id", "chunk_index", name="uq_file_chunk"),
    )
