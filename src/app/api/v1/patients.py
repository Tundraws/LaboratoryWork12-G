from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.crud.patient import create_patient, delete_patient, get_patient, list_patients, update_patient
from src.app.dependencies import get_current_user, require_roles
from src.app.core.database import get_db
from src.app.models.user import User, UserRole
from src.app.schemas.patient import PatientCreate, PatientRead, PatientUpdate

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("", response_model=list[PatientRead])
async def get_patients(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[PatientRead]:
    """Return patients list with role-aware filtering."""
    patients = await list_patients(db)
    if current_user.role == UserRole.admin:
        return patients
    if current_user.role == UserRole.doctor:
        return patients
    if current_user.role == UserRole.patient:
        return [patient for patient in patients if patient.id == current_user.patient_id]
    return []


@router.post("", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
async def post_patient(
    payload: PatientCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
) -> PatientRead:
    """Create a new patient (admin only)."""
    return await create_patient(db, payload)


@router.get("/{patient_id}", response_model=PatientRead)
async def get_patient_by_id(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PatientRead:
    """Return patient details by id with role checks."""
    patient = await get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    if current_user.role == UserRole.patient and current_user.patient_id != patient.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot view other patients")
    return patient


@router.put("/{patient_id}", response_model=PatientRead)
async def put_patient(
    patient_id: int,
    payload: PatientUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
) -> PatientRead:
    """Update patient by id (admin only)."""
    patient = await get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    return await update_patient(db, patient, payload)


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_patient(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
) -> None:
    """Delete patient by id (admin only)."""
    patient = await get_patient(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    await delete_patient(db, patient)
