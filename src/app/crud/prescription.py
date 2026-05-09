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
