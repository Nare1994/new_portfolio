from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps
from src.schemas.auth import Token, UserCreate, UserLogin, UserResponse
from src.services.auth import AuthService
from src.repositories.user import UserRepository
from src.core.database import get_db

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(
        *,
        db: AsyncSession = Depends(get_db),
        user_in: UserCreate,
) -> Any:
    """
    Регистрация нового пользователя
    """
    user_repo = UserRepository(db)

    # Проверяем, существует ли пользователь
    existing_user = await user_repo.get_by_email(email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )

    # Создаём пользователя
    auth_service = AuthService(user_repo)
    user = await auth_service.register_user(user_in)

    return user


@router.post("/login", response_model=Token)
async def login(
        *,
        db: AsyncSession = Depends(get_db),
        user_in: UserLogin,
) -> Any:
    """
    Вход в систему
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    # Аутентификация
    user = await auth_service.authenticate_user(
        email=user_in.email,
        password=user_in.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Создаём токены
    tokens = await auth_service.create_tokens(user_id=str(user.id))
    return tokens


@router.post("/refresh", response_model=Token)
async def refresh_token(
        *,
        db: AsyncSession = Depends(get_db),
        refresh_token: str,
) -> Any:
    """
    Обновление access токена
    """
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)

    new_tokens = await auth_service.refresh_tokens(refresh_token)
    if not new_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный refresh токен",
        )

    return new_tokens


@router.get("/me", response_model=UserResponse)
async def read_users_me(
        current_user=Depends(deps.get_current_active_user),
) -> Any:
    """
    Получить информацию о текущем пользователе
    """
    return current_user