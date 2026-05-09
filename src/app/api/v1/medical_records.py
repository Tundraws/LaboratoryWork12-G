from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.crud.medical_record import create_medical_record, list_medical_records
from src.app.dependencies import require_roles
from src.app.models.user import User, UserRole
from src.app.schemas.medical_record import MedicalRecordCreate, MedicalRecordRead

router = APIRouter(prefix="/medical-records", tags=["medical_records"])


@router.get("", response_model=list[MedicalRecordRead])
async def get_records(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> list[MedicalRecordRead]:
    """Return medical records for admin and doctor roles."""
    return await list_medical_records(db)


@router.post("", response_model=MedicalRecordRead, status_code=status.HTTP_201_CREATED)
async def post_record(
    payload: MedicalRecordCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> MedicalRecordRead:
    """Create medical record (admin or doctor)."""
    return await create_medical_record(db, payload)
