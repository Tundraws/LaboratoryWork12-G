from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.crud.appointment import (
    create_appointment,
    delete_appointment,
    get_appointment,
    list_appointments,
    update_appointment,
)
from src.app.dependencies import get_current_user, require_roles
from src.app.models.doctor import Doctor
from src.app.models.patient import Patient
from src.app.models.user import User, UserRole
from src.app.schemas.appointment import AppointmentCreate, AppointmentRead, AppointmentUpdate

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.get("", response_model=list[AppointmentRead])
async def get_appointments(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> list[AppointmentRead]:
    """Return appointments for admin and doctor roles."""
    return await list_appointments(db)


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
async def post_appointment(
    payload: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AppointmentRead:
    """Create appointment with role constraints."""
    if current_user.role not in {UserRole.admin, UserRole.doctor}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    if current_user.role == UserRole.doctor and current_user.doctor_id != payload.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor can create only own appointments")
    patient = await db.execute(select(Patient).where(Patient.id == payload.patient_id))
    if patient.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    doctor = await db.execute(select(Doctor).where(Doctor.id == payload.doctor_id))
    if doctor.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return await create_appointment(db, payload)


@router.get("/{appointment_id}", response_model=AppointmentRead)
async def get_appointment_by_id(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AppointmentRead:
    """Return appointment by id with role checks."""
    item = await get_appointment(db, appointment_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    if current_user.role == UserRole.doctor and current_user.doctor_id != item.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view other appointments")
    if current_user.role == UserRole.patient and current_user.patient_id != item.patient_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view other appointments")
    return item


@router.put("/{appointment_id}", response_model=AppointmentRead)
async def put_appointment(
    appointment_id: int,
    payload: AppointmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> AppointmentRead:
    """Update appointment with role-aware ownership checks."""
    item = await get_appointment(db, appointment_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    if current_user.role == UserRole.patient:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    if current_user.role == UserRole.doctor and (
        current_user.doctor_id != item.doctor_id or current_user.doctor_id != payload.doctor_id
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update other appointments")
    return await update_appointment(db, item, payload)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_appointment(
    appointment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete appointment by id with role checks."""
    item = await get_appointment(db, appointment_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found")
    if current_user.role == UserRole.doctor and current_user.doctor_id != item.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete other appointments")
    if current_user.role == UserRole.patient:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    await delete_appointment(db, item)
