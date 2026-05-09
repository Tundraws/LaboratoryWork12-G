from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.crud.doctor import create_doctor, delete_doctor, get_doctor, list_doctors
from src.app.dependencies import get_current_user, require_roles
from src.app.models.user import User, UserRole
from src.app.schemas.doctor import DoctorCreate, DoctorRead

router = APIRouter(prefix="/doctors", tags=["doctors"])


@router.get("", response_model=list[DoctorRead])
async def get_doctors(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> list[DoctorRead]:
    """Return doctors list for admin or doctor."""
    return await list_doctors(db)


@router.post("", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
async def post_doctor(
    payload: DoctorCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
) -> DoctorRead:
    """Create doctor profile (admin only)."""
    return await create_doctor(db, payload)


@router.get("/{doctor_id}", response_model=DoctorRead)
async def get_doctor_by_id(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DoctorRead:
    """Get doctor details by id with role checks."""
    doctor = await get_doctor(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    if current_user.role == UserRole.doctor and current_user.doctor_id != doctor.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view other doctors")
    if current_user.role == UserRole.patient:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    return doctor


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_doctor(
    doctor_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
) -> None:
    """Delete doctor by id (admin only)."""
    doctor = await get_doctor(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    await delete_doctor(db, doctor)
