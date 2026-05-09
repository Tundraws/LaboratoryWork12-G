from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.doctor import Doctor
from src.app.schemas.doctor import DoctorCreate


async def create_doctor(db: AsyncSession, payload: DoctorCreate) -> Doctor:
    doctor = Doctor(**payload.model_dump())
    db.add(doctor)
    await db.commit()
    await db.refresh(doctor)
    return doctor


async def list_doctors(db: AsyncSession) -> list[Doctor]:
    result = await db.execute(select(Doctor))
    return list(result.scalars().all())


async def get_doctor(db: AsyncSession, doctor_id: int) -> Doctor | None:
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    return result.scalar_one_or_none()


async def delete_doctor(db: AsyncSession, doctor: Doctor) -> None:
    await db.delete(doctor)
    await db.commit()
