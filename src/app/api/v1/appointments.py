from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.crud.appointment import create_appointment, list_appointments
from src.app.dependencies import require_roles
from src.app.models.user import User, UserRole
from src.app.schemas.appointment import AppointmentCreate, AppointmentRead

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
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> AppointmentRead:
    """Create appointment (admin or doctor)."""
    return await create_appointment(db, payload)
