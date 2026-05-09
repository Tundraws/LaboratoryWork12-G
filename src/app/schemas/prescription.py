from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator


class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    medication_name: str
    dosage: str
    issue_date: date
    valid_until: date

    @field_validator("valid_until")
    @classmethod
    def validate_valid_until(cls, value: date, info) -> date:
        issue_date = info.data.get("issue_date")
        if issue_date and value < issue_date:
            raise ValueError("valid_until cannot be earlier than issue_date")
        return value


class PrescriptionRead(PrescriptionCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
