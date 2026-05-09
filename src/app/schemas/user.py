from pydantic import BaseModel, EmailStr

from src.app.models.user import UserRole


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    patient_id: int | None = None
    doctor_id: int | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
