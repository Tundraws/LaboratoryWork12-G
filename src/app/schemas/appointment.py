from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_datetime: datetime
    status: Literal["scheduled", "completed", "cancelled"]
    complaint: str
    diagnosis: str | None = None

    @field_validator("appointment_datetime")
    @classmethod
    def validate_appointment_datetime(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        if value < datetime.now(timezone.utc):
            raise ValueError("appointment_datetime cannot be in the past")
        return value.astimezone(timezone.utc).replace(tzinfo=None)


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(AppointmentBase):
    pass


class AppointmentRead(AppointmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
