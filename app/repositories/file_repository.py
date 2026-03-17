from typing import List

from sqlalchemy.orm import Session

from app.models.file import FileModel, FileContent
from sqlalchemy.sql import func


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, file: FileModel):
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

    def get_all_by_user_id(self, current_user_id: int) -> List[FileModel]:
        return (
            self.db.query(FileModel).filter(FileModel.user_id == current_user_id).all()
        )

    def get_by_id_and_user_id(self, file_id: int, current_user_id: int) -> FileModel:
        return (
            self.db.query(FileModel)
            .filter(FileModel.id == file_id and FileModel.user_id == current_user_id)
            .first()
        )

    def delete(self, file: FileModel):
        self.db.delete(file)
        self.db.commit()

    def create_file_content(self, file_content: FileContent) -> FileContent:
        self.db.add(file_content)
        self.db.commit()
        self.db.refresh(file_content)
        return file_content

    def add(self, record):
        self.db.add(record)

    def commit(self):
        self.db.commit()

    def refresh(self, record):
        self.db.refresh(record)

    def search_files_content(self, q: str):
        return (
            self.db.query(FileModel)
            .join(FileContent)
            .filter(
                FileContent.content_tsv.op("@@")(func.plainto_tsquery("english", q))
            )
            .all()
        )
