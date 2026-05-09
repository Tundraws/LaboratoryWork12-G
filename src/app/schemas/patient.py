from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr


class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    phone: str
    email: EmailStr
    address: str
    insurance_policy: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(PatientBase):
    pass


class PatientRead(PatientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
