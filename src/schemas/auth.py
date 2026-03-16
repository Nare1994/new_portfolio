from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

# Токены
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str | None = None

# Регистрация и вход
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Ответы
class UserResponse(BaseModel):
    id: UUID  # Изменено с str на UUID
    email: EmailStr
    full_name: str | None = None
    is_active: bool
    is_superuser: bool

    model_config = ConfigDict(
        from_attributes=True,
        # Автоматически конвертировать UUID в строку при сериализации
        json_encoders={
            UUID: str
        }
    )