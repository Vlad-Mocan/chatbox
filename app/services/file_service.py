from fastapi import UploadFile
from sqlalchemy.orm import Session
from pathlib import Path
import uuid

from app.exceptions.custom_exceptions import (
    FileNotFoundException,
    FilenameMissingException,
)
from app.models.file import FileModel, FileContent
from app.repositories.file_repository import FileRepository
from sqlalchemy.sql import func

UPLOAD_DIR = Path("files")


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

        file_record = FileModel(
            user_id=current_user_id,
            original_name=file.filename,
            random_name=file_disk_info["random_filename"],
            content_type=file.content_type,
            size=file.size,
            path=str(file_disk_info["full_path"]),
        )

        saved_file = self.file_repo.create(file_record)

        content = file_disk_info["content"]
        try:
            text_content = content.decode("utf-8", errors="ignore")
        except UnicodeDecodeError:
            text_content = ""

        if text_content:
            content_entry = FileContent(
                file_id=file_record.id,
                content_tsv=func.to_tsvector("english", text_content),
            )
            self.file_repo.add(content_entry)

        self.file_repo.commit()
        self.file_repo.refresh(file_record)
        return saved_file

    def list_files_information_for_user(self, current_user_id: int):
        files = self.file_repo.get_all_by_user_id(current_user_id)

        if not files:
            raise FileNotFoundException()

        return files

    async def delete_file(self, file_id, current_user_id):
        file_entry = self.file_repo.get_by_id_and_user_id(file_id, current_user_id)

        if not file_entry:
            raise FileNotFoundException()

        self.file_repo.delete(file_entry)

        try:
            Path(file_entry.path).unlink(missing_ok=True)
        except OSError as e:
            print(f"File record deleted but disk file could not be removed: {e}")

    def search_file_content(self, q: str):
        return self.file_repo.search_files_content(q)
