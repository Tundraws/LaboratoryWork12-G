from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.medical_record import MedicalRecord
from src.app.schemas.medical_record import MedicalRecordCreate


async def create_medical_record(db: AsyncSession, payload: MedicalRecordCreate) -> MedicalRecord:
    item = MedicalRecord(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


async def list_medical_records(db: AsyncSession) -> list[MedicalRecord]:
    result = await db.execute(select(MedicalRecord))
    return list(result.scalars().all())


async def get_medical_record(db: AsyncSession, record_id: int) -> MedicalRecord | None:
    result = await db.execute(select(MedicalRecord).where(MedicalRecord.id == record_id))
    return result.scalar_one_or_none()


async def delete_medical_record(db: AsyncSession, item: MedicalRecord) -> None:
    await db.delete(item)
    await db.commit()
