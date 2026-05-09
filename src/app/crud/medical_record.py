from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.medical_record import MedicalRecord
from src.app.schemas.medical_record import MedicalRecordCreate, MedicalRecordUpdate


async def create_medical_record(db: AsyncSession, payload: MedicalRecordCreate) -> MedicalRecord:
    item = MedicalRecord(**payload.model_dump())
    db.add(item)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to create medical record") from exc
    await db.refresh(item)
    return item


async def list_medical_records(db: AsyncSession) -> list[MedicalRecord]:
    result = await db.execute(select(MedicalRecord))
    return list(result.scalars().all())


async def get_medical_record(db: AsyncSession, record_id: int) -> MedicalRecord | None:
    result = await db.execute(select(MedicalRecord).where(MedicalRecord.id == record_id))
    return result.scalar_one_or_none()


async def update_medical_record(db: AsyncSession, item: MedicalRecord, payload: MedicalRecordUpdate) -> MedicalRecord:
    for key, value in payload.model_dump().items():
        setattr(item, key, value)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to update medical record") from exc
    await db.refresh(item)
    return item


async def delete_medical_record(db: AsyncSession, item: MedicalRecord) -> None:
    await db.delete(item)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to delete medical record") from exc
