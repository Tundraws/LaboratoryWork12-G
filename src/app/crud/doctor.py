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
