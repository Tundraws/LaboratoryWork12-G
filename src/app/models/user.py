import enum

from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.patient, nullable=False)
    patient_id: Mapped[int | None] = mapped_column(ForeignKey("patients.id", ondelete="SET NULL"), nullable=True, index=True)
    doctor_id: Mapped[int | None] = mapped_column(ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True, index=True)
