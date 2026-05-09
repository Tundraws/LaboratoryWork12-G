from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.prescription import Prescription
from src.app.schemas.prescription import PrescriptionCreate, PrescriptionUpdate


async def create_prescription(db: AsyncSession, payload: PrescriptionCreate) -> Prescription:
    prescription = Prescription(**payload.model_dump())
    db.add(prescription)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to create prescription") from exc
    await db.refresh(prescription)
    return prescription


async def list_prescriptions(db: AsyncSession) -> list[Prescription]:
    result = await db.execute(select(Prescription))
    return list(result.scalars().all())


async def get_prescription(db: AsyncSession, prescription_id: int) -> Prescription | None:
    result = await db.execute(select(Prescription).where(Prescription.id == prescription_id))
    return result.scalar_one_or_none()


async def update_prescription(db: AsyncSession, prescription: Prescription, payload: PrescriptionUpdate) -> Prescription:
    for key, value in payload.model_dump().items():
        setattr(prescription, key, value)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to update prescription") from exc
    await db.refresh(prescription)
    return prescription


async def delete_prescription(db: AsyncSession, prescription: Prescription) -> None:
    await db.delete(prescription)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to delete prescription") from exc
