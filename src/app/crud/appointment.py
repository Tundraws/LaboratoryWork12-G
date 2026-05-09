from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.appointment import Appointment
from src.app.schemas.appointment import AppointmentCreate, AppointmentUpdate


async def create_appointment(db: AsyncSession, payload: AppointmentCreate) -> Appointment:
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to create appointment") from exc
    await db.refresh(appointment)
    return appointment


async def list_appointments(db: AsyncSession) -> list[Appointment]:
    result = await db.execute(select(Appointment))
    return list(result.scalars().all())


async def get_appointment(db: AsyncSession, appointment_id: int) -> Appointment | None:
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    return result.scalar_one_or_none()


async def update_appointment(db: AsyncSession, appointment: Appointment, payload: AppointmentUpdate) -> Appointment:
    for key, value in payload.model_dump().items():
        setattr(appointment, key, value)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to update appointment") from exc
    await db.refresh(appointment)
    return appointment


async def delete_appointment(db: AsyncSession, appointment: Appointment) -> None:
    await db.delete(appointment)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to delete appointment") from exc
