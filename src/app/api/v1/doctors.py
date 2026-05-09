from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.crud.doctor import create_doctor, list_doctors
from src.app.dependencies import require_roles
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
