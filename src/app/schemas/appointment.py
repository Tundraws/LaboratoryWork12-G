from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_datetime: datetime
    status: str
    complaint: str
    diagnosis: str | None = None


class AppointmentRead(AppointmentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
