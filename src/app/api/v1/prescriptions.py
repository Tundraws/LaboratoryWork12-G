from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.crud.prescription import create_prescription, delete_prescription, get_prescription, list_prescriptions
from src.app.dependencies import get_current_user
from src.app.models.user import User, UserRole
from src.app.schemas.prescription import PrescriptionCreate, PrescriptionRead

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])


@router.get("", response_model=list[PrescriptionRead])
async def get_prescriptions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PrescriptionRead]:
    """Return prescriptions list based on role."""
    items = await list_prescriptions(db)
    if current_user.role == UserRole.admin:
        return items
    if current_user.role == UserRole.doctor:
        return [item for item in items if item.doctor_id == current_user.doctor_id]
    if current_user.role == UserRole.patient:
        return [item for item in items if item.patient_id == current_user.patient_id]
    return []


@router.post("", response_model=PrescriptionRead, status_code=status.HTTP_201_CREATED)
async def post_prescription(
    payload: PrescriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PrescriptionRead:
    """Create prescription with role constraints."""
    if current_user.role not in {UserRole.admin, UserRole.doctor}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    if current_user.role == UserRole.doctor and current_user.doctor_id != payload.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Doctor can create only own prescriptions")
    return await create_prescription(db, payload)


@router.get("/{prescription_id}", response_model=PrescriptionRead)
async def get_prescription_by_id(
    prescription_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PrescriptionRead:
    """Return prescription by id with role checks."""
    item = await get_prescription(db, prescription_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
    if current_user.role == UserRole.doctor and current_user.doctor_id != item.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view other prescriptions")
    if current_user.role == UserRole.patient and current_user.patient_id != item.patient_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view other prescriptions")
    return item


@router.delete("/{prescription_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_prescription(
    prescription_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete prescription by id with role checks."""
    item = await get_prescription(db, prescription_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prescription not found")
    if current_user.role == UserRole.doctor and current_user.doctor_id != item.doctor_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete other prescriptions")
    if current_user.role == UserRole.patient:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
    await delete_prescription(db, item)
