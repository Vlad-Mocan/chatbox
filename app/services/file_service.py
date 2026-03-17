import logging
from pathlib import Path
import uuid
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import UploadFile

from app.exceptions.custom_exceptions import (
    FileNotFoundException,
    FilenameMissingException,
)
from app.database.schema import FileModel, FileContent
from app.repositories.file_repository import FileRepository

UPLOAD_DIR = Path("files")

logger = logging.getLogger(__name__)


class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.file_repo = FileRepository(db)

    async def upload_file_to_disk(self, file: UploadFile, current_user_id: int):
        extension = Path(file.filename).suffix
        random_filename = f"{uuid.uuid4()}{extension}"
        full_path = UPLOAD_DIR / str(current_user_id) / random_filename
        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            content = await file.read()
            full_path.write_bytes(content)
        finally:
            await file.close()

        return {
            "random_filename": random_filename,
            "full_path": full_path,
            "content": content,
        }

    async def upload_file(self, file: UploadFile, current_user_id: int):
        if not file.filename:
            raise FilenameMissingException()

        file_disk_info = await self.upload_file_to_disk(file, current_user_id)
        content = file_disk_info["content"]

        is_text_file = file.content_type and file.content_type.startswith("text/")
        if is_text_file:
            text_content = content.decode("utf-8", errors="ignore")
        else:
            text_content = ""

        file_record = FileModel(
            user_id=current_user_id,
            original_name=file.filename,
            random_name=file_disk_info["random_filename"],
            content_type=file.content_type or "application/octet-stream",
            size=len(content),
            path=str(file_disk_info["full_path"]),
        )

        content_entry = None
        if text_content:
            content_entry = FileContent(
                content_tsv=func.to_tsvector("english", text_content),
            )

        try:
            return self.file_repo.create_with_optional_content(
                file_record, content_entry
            )
        except Exception:
            file_disk_info["full_path"].unlink(missing_ok=True)
            raise

    def list_files_information_for_user(self, current_user_id: int):
        return self.file_repo.get_all_by_user_id(current_user_id)

    def get_file_content(self, file_id: int, current_user_id: int):
        file_entry = self.file_repo.get_by_id_and_user_id(file_id, current_user_id)

        if not file_entry:
            raise FileNotFoundException()

        return file_entry

    async def delete_file(self, file_id, current_user_id):
        file_entry = self.file_repo.get_by_id_and_user_id(file_id, current_user_id)

        if not file_entry:
            raise FileNotFoundException()

        self.file_repo.delete(file_entry)

        try:
            Path(file_entry.path).unlink(missing_ok=True)
        except OSError as e:
            logger.warning(
                "File record deleted but disk file could not be removed: %s", e
            )

    def search_file_content(
        self, q: str, limit: int, offset: int, current_user_id: int
    ):
        if not q:
            return []

        limit = max(1, min(limit, 100))
        offset = max(0, offset)

        tsquery = func.websearch_to_tsquery("english", q)
        rank = func.ts_rank_cd(FileContent.content_tsv, tsquery).label("rank")

        return self.file_repo.search_files_content(
            rank, tsquery, limit, offset, current_user_id
        )
