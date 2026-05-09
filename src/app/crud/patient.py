from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.patient import Patient
from src.app.schemas.patient import PatientCreate, PatientUpdate


async def create_patient(db: AsyncSession, payload: PatientCreate) -> Patient:
    patient = Patient(**payload.model_dump())
    db.add(patient)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to create patient") from exc
    await db.refresh(patient)
    return patient


async def list_patients(db: AsyncSession) -> list[Patient]:
    result = await db.execute(select(Patient))
    return list(result.scalars().all())


async def get_patient(db: AsyncSession, patient_id: int) -> Patient | None:
    result = await db.execute(select(Patient).where(Patient.id == patient_id))
    return result.scalar_one_or_none()


async def update_patient(db: AsyncSession, patient: Patient, payload: PatientUpdate) -> Patient:
    for key, value in payload.model_dump().items():
        setattr(patient, key, value)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to update patient") from exc
    await db.refresh(patient)
    return patient


async def delete_patient(db: AsyncSession, patient: Patient) -> None:
    await db.delete(patient)
    try:
        await db.commit()
    except SQLAlchemyError as exc:
        await db.rollback()
        raise RuntimeError("Failed to delete patient") from exc
