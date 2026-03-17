from app.database.session import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TSVECTOR


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

    file_id = Column(Integer, ForeignKey("files.id"), primary_key=True)
    content_tsv = Column(TSVECTOR, nullable=False)

    __table_args__ = (
        Index("idx_file_content_tsv", "content_tsv", postgresql_using="gin"),
    )
