from pydantic import BaseModel, ConfigDict, EmailStr


class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    specialty: str
    phone: str
    email: EmailStr
    schedule: str


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(DoctorBase):
    pass


class DoctorRead(DoctorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
