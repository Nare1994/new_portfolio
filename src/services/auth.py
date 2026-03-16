from typing import Optional
from jose import jwt, JWTError
from src.core import security
from src.core.config import settings
from src.repositories.user import UserRepository
from src.schemas.auth import UserCreate, Token
from src.models.user import User


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, user_in: UserCreate) -> User:
        """
        Регистрация нового пользователя
        """
        hashed_password = security.get_password_hash(user_in.password)

        user = await self.user_repo.create(
            email=user_in.email,
            hashed_password=hashed_password,
            full_name=user_in.full_name
        )
        return user

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """
        Аутентификация пользователя
        """
        user = await self.user_repo.get_by_email(email=email)
        if not user:
            return None
        if not security.verify_password(password, user.hashed_password):
            return None
        return user

    async def create_tokens(self, user_id: str) -> Token:
        """
        Создание access и refresh токенов
        """
        access_token = security.create_access_token(user_id)
        refresh_token = security.create_refresh_token(user_id)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

    async def refresh_tokens(self, refresh_token: str) -> Optional[Token]:
        """
        Обновление токенов по refresh токену
        """
        try:
            payload = jwt.decode(
                refresh_token,
                settings.SECRET_KEY,
                algorithms=[security.ALGORITHM]
            )
            user_id: str = payload.get("sub")
            token_type: str = payload.get("type", "")

            if user_id is None or token_type != "refresh":
                return None

        except JWTError:
            return None

        user = await self.user_repo.get_by_id(user_id)
        if not user:
            return None

        return await self.create_tokens(user_id)