from typing import List

from sqlalchemy.orm import Session

from app.database.schema import FileModel, FileContent

from app.models.file import FileResponse


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_with_chunks(
        self, file_record: FileModel, content_entries: List[FileContent]
    ) -> FileModel:
        self.db.add(file_record)
        self.db.flush()

        if content_entries:
            for entry in content_entries:
                entry.file_id = file_record.id

            self.db.add_all(content_entries)

        try:
            self.db.commit()
            self.db.refresh(file_record)
            return file_record
        except Exception:
            self.db.rollback()
            raise

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

    def search_files_content(
        self, rank, tsquery, limit: int, offset: int, current_user_id: int
    ) -> List[FileModel]:
        rows = (
            self.db.query(FileModel, rank)
            .join(FileContent, FileContent.file_id == FileModel.id)
            .filter(
                FileModel.user_id == current_user_id,
                FileContent.content_tsv.op("@@")(tsquery),
            )
            .order_by(rank.desc(), FileModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        results: list[dict] = []

        for file_record, file_rank in rows:
            results.append(
                {
                    "rank": float(file_rank or 0.0),
                    "file": FileResponse.model_validate(file_record),
                }
            )
        return results

    def search_files_content_semantic(
        self, query_embedding, limit: int, offset: int, current_user_id: int
    ):
        similarity = (1 - FileContent.embedding.cosine_distance(query_embedding)).label(
            "similarity"
        )

        rows = (
            self.db.query(FileModel, similarity)
            .join(FileContent, FileContent.file_id == FileModel.id)
            .filter(FileModel.user_id == current_user_id)
            .order_by(similarity.desc(), FileModel.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        results = []
        for file_record, sim in rows:
            results.append(
                {
                    "similarity": float(sim or 0.0),
                    "file": FileResponse.model_validate(file_record),
                }
            )

        return results
