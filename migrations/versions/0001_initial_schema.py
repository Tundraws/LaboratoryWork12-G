"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-05-09
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
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


def downgrade() -> None:
    op.drop_index("ix_doctors_specialty", table_name="doctors")
    op.drop_index("ix_doctors_email", table_name="doctors")
    op.drop_table("doctors")
    op.drop_index("ix_patients_insurance_policy", table_name="patients")
    op.drop_index("ix_patients_email", table_name="patients")
    op.drop_table("patients")
