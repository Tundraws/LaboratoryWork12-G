from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.crud.prescription import create_prescription, list_prescriptions
from src.app.dependencies import require_roles
from src.app.models.user import User, UserRole
from src.app.schemas.prescription import PrescriptionCreate, PrescriptionRead

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"])


@router.get("", response_model=list[PrescriptionRead])
async def get_prescriptions(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> list[PrescriptionRead]:
    """Return prescriptions for admin and doctor roles."""
    return await list_prescriptions(db)


@router.post("", response_model=PrescriptionRead, status_code=status.HTTP_201_CREATED)
async def post_prescription(
    payload: PrescriptionCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> PrescriptionRead:
    """Create prescription (admin or doctor)."""
    return await create_prescription(db, payload)
