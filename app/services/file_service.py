from fastapi import UploadFile
from sqlalchemy.orm import Session
from pathlib import Path
import uuid

from app.exceptions.custom_exceptions import (
    FileNotFoundException,
    FilenameMissingException,
)
from app.models.file import FileModel
from app.models.user import User
from app.repositories.file_repository import FileRepository


class FileService:
    def __init__(self, db: Session):
        self.db = db
        self.file_repo = FileRepository(db)

    async def upload_file(self, file: UploadFile, current_user_id: int):
        if not file.filename:
            raise FilenameMissingException()

        extension = Path(file.filename).suffix
        random_filename = f"{uuid.uuid4()}{extension}"

        directory = Path("files") / str(current_user_id)
        full_path = directory / random_filename

        directory.mkdir(parents=True, exist_ok=True)
        full_path.write_bytes(await file.read())

        file_record = FileModel(
            user_id=current_user_id,
            original_name=file.filename,
            random_name=random_filename,
            content_type=file.content_type,
            size=file.size,
            path=str(full_path),
        )

        saved_file = self.file_repo.create(file_record)
        return saved_file

    def list_files_information_for_user(self, current_user_id: int):
        files = self.file_repo.get_all_by_user_id(current_user_id)

        if not files:
            raise FileNotFoundException()

    async def delete_file(self, file_id, current_user_id):
        file_entry = self.file_repo.get_by_id_and_user_id(file_id, current_user_id)

        if not file_entry:
            raise FileNotFoundException()

        file_path = Path(file_entry.path)
        if file_path.exists():
            file_path.unlink()
        else:
            print("File doesn't exist on the disk!")

        self.file_repo.delete(file_entry)
