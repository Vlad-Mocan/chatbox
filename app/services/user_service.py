from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import TokenResponse, UserCreate, UserLogIn, UserResponse
from app.core.security import create_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.exceptions.custom_exceptions import EmailAlreadyExistsException, InvalidCredentialsException

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def create_user(self, user_data: UserCreate) -> TokenResponse:
        existing = self.user_repo.get_by_email(user_data.email)
        if existing:
            raise EmailAlreadyExistsException(user_data.email)
        
        hashed_password = hash_password(user_data.password)
        
        new_user = User(
            email=user_data.email,
            password=hashed_password,
            name=user_data.name,
        )

        user = self.user_repo.create(new_user)

        return TokenResponse(
            access_token=create_token(user.id),
            user=UserResponse.model_validate(user)
        )
    
    def login_user(self, user_data: UserLogIn) -> TokenResponse:
        user = self.user_repo.get_by_email(user_data.email)

        if not user or not verify_password(user_data.password, user.password):
            raise InvalidCredentialsException()
        
        return TokenResponse(
            access_token=create_token(user.id),
            user=UserResponse.model_validate(user)
        )
    
