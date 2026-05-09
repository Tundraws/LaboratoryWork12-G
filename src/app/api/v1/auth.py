from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.core.security import create_access_token, hash_password, verify_password
from src.app.models.doctor import Doctor
from src.app.models.patient import Patient
from src.app.models.user import User, UserRole
from src.app.schemas.user import TokenResponse, UserLogin, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Register new user and return JWT token."""
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already used")

    if payload.role == UserRole.patient and payload.patient_id is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="patient_id is required")
    if payload.role == UserRole.doctor and payload.doctor_id is None:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="doctor_id is required")

    if payload.patient_id is not None:
        patient = await db.execute(select(Patient).where(Patient.id == payload.patient_id))
        if patient.scalar_one_or_none() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if payload.doctor_id is not None:
        doctor = await db.execute(select(Doctor).where(Doctor.id == payload.doctor_id))
        if doctor.scalar_one_or_none() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=payload.role,
        patient_id=payload.patient_id,
        doctor_id=payload.doctor_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    token = create_access_token(subject=str(user.id), role=user.role.value)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Authenticate user and return JWT token."""
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=str(user.id), role=user.role.value)
    return TokenResponse(access_token=token)
