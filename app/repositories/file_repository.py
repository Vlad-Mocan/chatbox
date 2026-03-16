from typing import List

from sqlalchemy.orm import Session

from app.models.file import FileModel


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, file: FileModel):
        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)
        return file

    def get_by_user_id(self, current_user_id: int) -> List[FileModel]:
        return (
            self.db.query(FileModel).filter(FileModel.user_id == current_user_id).all()
        )
