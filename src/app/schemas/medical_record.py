from datetime import date

from pydantic import BaseModel, ConfigDict


class MedicalRecordBase(BaseModel):
    patient_id: int
    doctor_id: int
    record_date: date
    diagnosis: str
    treatment: str
    notes: str | None = None


class MedicalRecordCreate(MedicalRecordBase):
    pass


class MedicalRecordUpdate(MedicalRecordBase):
    pass


class MedicalRecordRead(MedicalRecordBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
