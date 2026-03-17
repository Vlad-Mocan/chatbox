from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.schemas.file import FileResponse
from app.services.file_service import FileService

router = APIRouter()


@router.post("", response_model=FileResponse, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return await FileService(db).upload_file(file, current_user.id)


@router.get("", response_model=list[FileResponse], status_code=200)
def get_files_information_for_user(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return FileService(db).list_files_information_for_user(current_user.id)


@router.get("/search", response_model=list[FileResponse])
def search_file_content(
    q: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return FileService(db).search_file_content(q, current_user.id)


@router.delete("/{file_id}", status_code=204)
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    await FileService(db).delete_file(file_id, current_user.id)
