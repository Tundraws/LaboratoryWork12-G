from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.prescription import Prescription
from src.app.schemas.prescription import PrescriptionCreate


async def create_prescription(db: AsyncSession, payload: PrescriptionCreate) -> Prescription:
    prescription = Prescription(**payload.model_dump())
    db.add(prescription)
    await db.commit()
    await db.refresh(prescription)
    return prescription


async def list_prescriptions(db: AsyncSession) -> list[Prescription]:
    result = await db.execute(select(Prescription))
    return list(result.scalars().all())


async def get_prescription(db: AsyncSession, prescription_id: int) -> Prescription | None:
    result = await db.execute(select(Prescription).where(Prescription.id == prescription_id))
    return result.scalar_one_or_none()


async def delete_prescription(db: AsyncSession, prescription: Prescription) -> None:
    await db.delete(prescription)
    await db.commit()
