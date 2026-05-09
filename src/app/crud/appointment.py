from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.appointment import Appointment
from src.app.schemas.appointment import AppointmentCreate


async def create_appointment(db: AsyncSession, payload: AppointmentCreate) -> Appointment:
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


async def list_appointments(db: AsyncSession) -> list[Appointment]:
    result = await db.execute(select(Appointment))
    return list(result.scalars().all())
