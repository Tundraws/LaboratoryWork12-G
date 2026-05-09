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


async def get_appointment(db: AsyncSession, appointment_id: int) -> Appointment | None:
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    return result.scalar_one_or_none()


async def delete_appointment(db: AsyncSession, appointment: Appointment) -> None:
    await db.delete(appointment)
    await db.commit()
