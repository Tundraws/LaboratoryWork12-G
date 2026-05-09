from datetime import date

from pydantic import BaseModel, ConfigDict


class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    medication_name: str
    dosage: str
    issue_date: date
    valid_until: date


class PrescriptionRead(PrescriptionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
