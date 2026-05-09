from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.doctor import Doctor
from src.app.schemas.doctor import DoctorCreate, DoctorUpdate


async def create_doctor(db: AsyncSession, payload: DoctorCreate) -> Doctor:
    doctor = Doctor(**payload.model_dump())
    db.add(doctor)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to create doctor") from exc
    await db.refresh(doctor)
    return doctor


async def list_doctors(db: AsyncSession) -> list[Doctor]:
    result = await db.execute(select(Doctor))
    return list(result.scalars().all())


async def get_doctor(db: AsyncSession, doctor_id: int) -> Doctor | None:
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    return result.scalar_one_or_none()


async def update_doctor(db: AsyncSession, doctor: Doctor, payload: DoctorUpdate) -> Doctor:
    for key, value in payload.model_dump().items():
        setattr(doctor, key, value)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to update doctor") from exc
    await db.refresh(doctor)
    return doctor


async def delete_doctor(db: AsyncSession, doctor: Doctor) -> None:
    await db.delete(doctor)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to delete doctor") from exc
