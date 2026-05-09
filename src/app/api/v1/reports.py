from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.core.database import get_db
from src.app.dependencies import require_roles
from src.app.models.appointment import Appointment
from src.app.models.doctor import Doctor
from src.app.models.patient import Patient
from src.app.models.prescription import Prescription
from src.app.models.user import User, UserRole

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/doctors/by-patients-count")
async def doctors_by_patients_count(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin)),
) -> list[dict[str, int | str]]:
    """Return doctors sorted by patient visits count."""
    query = (
        select(Doctor.id, Doctor.first_name, Doctor.last_name, func.count(Appointment.id).label("patients_count"))
        .join(Appointment, Appointment.doctor_id == Doctor.id)
        .group_by(Doctor.id)
        .order_by(func.count(Appointment.id).desc())
    )
    result = await db.execute(query)
    return [
        {
            "doctor_id": row.id,
            "doctor": f"{row.first_name} {row.last_name}",
            "patients_count": row.patients_count,
        }
        for row in result
    ]


@router.get("/patients/by-visits")
async def patients_by_visits(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> list[dict[str, int | str]]:
    """Return patients sorted by visits count."""
    query = (
        select(Patient.id, Patient.first_name, Patient.last_name, func.count(Appointment.id).label("visits_count"))
        .join(Appointment, Appointment.patient_id == Patient.id)
        .group_by(Patient.id)
        .order_by(func.count(Appointment.id).desc())
    )
    result = await db.execute(query)
    return [
        {"patient_id": row.id, "patient": f"{row.first_name} {row.last_name}", "visits_count": row.visits_count}
        for row in result
    ]


@router.get("/prescriptions/by-medication")
async def prescriptions_by_medication(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_roles(UserRole.admin, UserRole.doctor)),
) -> list[dict[str, int | str]]:
    """Return medication statistics by issued prescriptions."""
    query = (
        select(Prescription.medication_name, func.count(Prescription.id).label("issued_count"))
        .group_by(Prescription.medication_name)
        .order_by(func.count(Prescription.id).desc())
    )
    result = await db.execute(query)
    return [{"medication_name": row.medication_name, "issued_count": row.issued_count} for row in result]
