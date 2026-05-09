"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-09
"""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "patients",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("date_of_birth", sa.Date(), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("insurance_policy", sa.String(length=50), nullable=False),
    )
    op.create_index("ix_patients_email", "patients", ["email"], unique=True)
    op.create_index("ix_patients_insurance_policy", "patients", ["insurance_policy"], unique=True)

    op.create_table(
        "doctors",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(length=100), nullable=False),
        sa.Column("last_name", sa.String(length=100), nullable=False),
        sa.Column("specialty", sa.String(length=120), nullable=False),
        sa.Column("phone", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("schedule", sa.String(length=255), nullable=False),
    )
    op.create_index("ix_doctors_email", "doctors", ["email"], unique=True)
    op.create_index("ix_doctors_specialty", "doctors", ["specialty"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.Enum("admin", "doctor", "patient", name="userrole"), nullable=False),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.id", ondelete="SET NULL"), nullable=True),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id", ondelete="SET NULL"), nullable=True),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_patient_id", "users", ["patient_id"], unique=False)
    op.create_index("ix_users_doctor_id", "users", ["doctor_id"], unique=False)

    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("appointment_datetime", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("complaint", sa.String(length=400), nullable=False),
        sa.Column("diagnosis", sa.String(length=400), nullable=True),
    )
    op.create_index("ix_appointments_patient_id", "appointments", ["patient_id"], unique=False)
    op.create_index("ix_appointments_doctor_id", "appointments", ["doctor_id"], unique=False)
    op.create_index("ix_appointments_appointment_datetime", "appointments", ["appointment_datetime"], unique=False)

    op.create_table(
        "prescriptions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("medication_name", sa.String(length=255), nullable=False),
        sa.Column("dosage", sa.String(length=120), nullable=False),
        sa.Column("issue_date", sa.Date(), nullable=False),
        sa.Column("valid_until", sa.Date(), nullable=False),
    )
    op.create_index("ix_prescriptions_patient_id", "prescriptions", ["patient_id"], unique=False)
    op.create_index("ix_prescriptions_doctor_id", "prescriptions", ["doctor_id"], unique=False)
    op.create_index("ix_prescriptions_medication_name", "prescriptions", ["medication_name"], unique=False)

    op.create_table(
        "medical_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("patient_id", sa.Integer(), sa.ForeignKey("patients.id", ondelete="CASCADE"), nullable=False),
        sa.Column("doctor_id", sa.Integer(), sa.ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False),
        sa.Column("record_date", sa.Date(), nullable=False),
        sa.Column("diagnosis", sa.String(length=400), nullable=False),
        sa.Column("treatment", sa.String(length=400), nullable=False),
        sa.Column("notes", sa.String(length=1000), nullable=True),
    )
    op.create_index("ix_medical_records_patient_id", "medical_records", ["patient_id"], unique=False)
    op.create_index("ix_medical_records_doctor_id", "medical_records", ["doctor_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_medical_records_doctor_id", table_name="medical_records")
    op.drop_index("ix_medical_records_patient_id", table_name="medical_records")
    op.drop_table("medical_records")

    op.drop_index("ix_prescriptions_medication_name", table_name="prescriptions")
    op.drop_index("ix_prescriptions_doctor_id", table_name="prescriptions")
    op.drop_index("ix_prescriptions_patient_id", table_name="prescriptions")
    op.drop_table("prescriptions")

    op.drop_index("ix_appointments_appointment_datetime", table_name="appointments")
    op.drop_index("ix_appointments_doctor_id", table_name="appointments")
    op.drop_index("ix_appointments_patient_id", table_name="appointments")
    op.drop_table("appointments")

    op.drop_index("ix_users_doctor_id", table_name="users")
    op.drop_index("ix_users_patient_id", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")

    op.drop_index("ix_doctors_specialty", table_name="doctors")
    op.drop_index("ix_doctors_email", table_name="doctors")
    op.drop_table("doctors")

    op.drop_index("ix_patients_insurance_policy", table_name="patients")
    op.drop_index("ix_patients_email", table_name="patients")
    op.drop_table("patients")

    op.execute("DROP TYPE userrole")
