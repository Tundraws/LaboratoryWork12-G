from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.crud.medical_record import (
    create_medical_record,
    delete_medical_record,
    get_medical_record,
    list_medical_records,
    update_medical_record,
)
from src.app.dependencies import get_current_user
from src.app.models.doctor import Doctor
from src.app.models.patient import Patient
from src.app.models.user import User, UserRole
from src.app.schemas.medical_record import MedicalRecordCreate, MedicalRecordRead, MedicalRecordUpdate

router = APIRouter(prefix="/medical-records", tags=["medical_records"])


@router.get("", response_model=list[MedicalRecordRead])
async def get_records(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[MedicalRecordRead]:
    """Return medical records list based on role."""
    items = await list_medical_records(db)
    if current_user.role == UserRole.admin:
        return items
    if current_user.role == UserRole.doctor:
        return [item for item in items if item.doctor_id == current_user.doctor_id]
    if current_user.role == UserRole.patient:
        return [item for item in items if item.patient_id == current_user.patient_id]
    return []


@router.post("", response_model=MedicalRecordRead, status_code=status.HTTP_201_CREATED)
async def post_record(
    payload: MedicalRecordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MedicalRecordRead:
    """Create medical record with role constraints."""
    if current_user.role not in {UserRole.admin, UserRole.doctor}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    if current_user.role == UserRole.doctor and current_user.doctor_id != payload.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor can create only own records")
    patient = await db.execute(select(Patient).where(Patient.id == payload.patient_id))
    if patient.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    doctor = await db.execute(select(Doctor).where(Doctor.id == payload.doctor_id))
    if doctor.scalar_one_or_none() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    return await create_medical_record(db, payload)


@router.get("/{record_id}", response_model=MedicalRecordRead)
async def get_record_by_id(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MedicalRecordRead:
    """Return medical record by id with role checks."""
    item = await get_medical_record(db, record_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found")
    if current_user.role == UserRole.doctor and current_user.doctor_id != item.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view other records")
    if current_user.role == UserRole.patient and current_user.patient_id != item.patient_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view other records")
    return item


@router.put("/{record_id}", response_model=MedicalRecordRead)
async def put_record(
    record_id: int,
    payload: MedicalRecordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> MedicalRecordRead:
    """Update medical record by id with role-aware checks."""
    item = await get_medical_record(db, record_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found")
    if current_user.role == UserRole.patient:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    if current_user.role == UserRole.doctor and (
        current_user.doctor_id != item.doctor_id or current_user.doctor_id != payload.doctor_id
    ):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update other records")
    return await update_medical_record(db, item, payload)


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_record(
    record_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete medical record by id with role checks."""
    item = await get_medical_record(db, record_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found")
    if current_user.role == UserRole.doctor and current_user.doctor_id != item.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete other records")
    if current_user.role == UserRole.patient:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    await delete_medical_record(db, item)
