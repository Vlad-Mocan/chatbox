from typing import List, Optional

from sqlalchemy.orm import Session

from app.database.schema import FileModel, FileContent
from sqlalchemy.sql import func


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_with_optional_content(
        self, file_record: FileModel, content_entry: Optional[FileContent]
    ) -> FileModel:
        self.db.add(file_record)
        self.db.flush()

        if content_entry is not None:
            content_entry.file_id = file_record.id
            self.db.add(content_entry)

        self.db.commit()
        self.db.refresh(file_record)
        return file_record

    def get_all_by_user_id(self, current_user_id: int) -> List[FileModel]:
        return (
            self.db.query(FileModel).filter(FileModel.user_id == current_user_id).all()
        )

    def get_by_id_and_user_id(self, file_id: int, current_user_id: int) -> FileModel:
        return (
            self.db.query(FileModel)
            .filter(FileModel.id == file_id, FileModel.user_id == current_user_id)
            .first()
        )

    def delete(self, file: FileModel):
        self.db.delete(file)
        self.db.commit()

    def search_files_content(self, q: str, current_user_id: int) -> List[FileModel]:
        return (
            self.db.query(FileModel)
            .join(FileContent)
            .filter(
                FileModel.user_id == current_user_id,
                FileContent.content_tsv.op("@@")(func.plainto_tsquery("english", q)),
            )
            .all()
        )
