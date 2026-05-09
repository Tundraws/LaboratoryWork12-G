from datetime import date

from pydantic import BaseModel, ConfigDict


class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    record_date: date
    diagnosis: str
    treatment: str
    notes: str | None = None


class MedicalRecordRead(MedicalRecordCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
