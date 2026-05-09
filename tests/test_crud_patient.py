from datetime import date
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.exc import IntegrityError

from src.app.crud.patient import create_patient, delete_patient, get_patient, list_patients, update_patient
from src.app.models.patient import Patient
from src.app.schemas.patient import PatientCreate, PatientUpdate


@pytest.fixture
def patient_payload() -> PatientCreate:
    return PatientCreate(
        first_name="Ann",
        last_name="Melnikova",
        date_of_birth=date(2000, 1, 1),
        phone="+123456789",
        email="ann@example.com",
        address="Street 1",
        insurance_policy="1234567890123456",
    )


@pytest.mark.asyncio
async def test_create_patient_success(patient_payload: PatientCreate) -> None:
    db = SimpleNamespace(add=Mock(), commit=AsyncMock(), rollback=AsyncMock(), refresh=AsyncMock(), delete=AsyncMock())
    result = await create_patient(db, patient_payload)
    assert isinstance(result, Patient)
    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_patient_rolls_back_on_error(patient_payload: PatientCreate) -> None:
    db = SimpleNamespace(add=Mock(), commit=AsyncMock(side_effect=IntegrityError("stmt", "params", Exception("x"))), rollback=AsyncMock(), refresh=AsyncMock(), delete=AsyncMock())
    with pytest.raises(RuntimeError):
        await create_patient(db, patient_payload)
    db.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_patients() -> None:
    db = SimpleNamespace(execute=AsyncMock())
    patient = Patient(id=1, first_name="A", last_name="B", date_of_birth=date(2000, 1, 1), phone="1", email="a@b.c", address="x", insurance_policy="1")
    db.execute.return_value = SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: [patient]))
    result = await list_patients(db)
    assert len(result) == 1


@pytest.mark.asyncio
async def test_get_patient_found() -> None:
    db = SimpleNamespace(execute=AsyncMock())
    patient = Patient(id=5, first_name="A", last_name="B", date_of_birth=date(2000, 1, 1), phone="1", email="a@b.c", address="x", insurance_policy="1")
    db.execute.return_value = SimpleNamespace(scalar_one_or_none=lambda: patient)
    result = await get_patient(db, 5)
    assert result == patient


@pytest.mark.asyncio
async def test_update_patient_success() -> None:
    db = SimpleNamespace(commit=AsyncMock(), rollback=AsyncMock(), refresh=AsyncMock())
    patient = Patient(id=1, first_name="A", last_name="B", date_of_birth=date(2000, 1, 1), phone="1", email="a@b.c", address="x", insurance_policy="1")
    payload = PatientUpdate(
        first_name="New",
        last_name="Name",
        date_of_birth=date(2000, 1, 1),
        phone="2",
        email="new@example.com",
        address="new",
        insurance_policy="2",
    )
    result = await update_patient(db, patient, payload)
    assert result.first_name == "New"
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_patient_success() -> None:
    db = SimpleNamespace(delete=AsyncMock(), commit=AsyncMock(), rollback=AsyncMock())
    patient = Patient(id=1, first_name="A", last_name="B", date_of_birth=date(2000, 1, 1), phone="1", email="a@b.c", address="x", insurance_policy="1")
    await delete_patient(db, patient)
    db.delete.assert_awaited_once_with(patient)
    db.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_update_patient_rollback_on_error() -> None:
    db = SimpleNamespace(commit=AsyncMock(side_effect=IntegrityError("stmt", "params", Exception("x"))), rollback=AsyncMock(), refresh=AsyncMock())
    patient = Patient(id=1, first_name="A", last_name="B", date_of_birth=date(2000, 1, 1), phone="1", email="a@b.c", address="x", insurance_policy="1")
    payload = PatientUpdate(
        first_name="New",
        last_name="Name",
        date_of_birth=date(2000, 1, 1),
        phone="2",
        email="new@example.com",
        address="new",
        insurance_policy="2",
    )
    with pytest.raises(RuntimeError):
        await update_patient(db, patient, payload)
    db.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_delete_patient_rollback_on_error() -> None:
    db = SimpleNamespace(delete=AsyncMock(), commit=AsyncMock(side_effect=IntegrityError("stmt", "params", Exception("x"))), rollback=AsyncMock())
    patient = Patient(id=1, first_name="A", last_name="B", date_of_birth=date(2000, 1, 1), phone="1", email="a@b.c", address="x", insurance_policy="1")
    with pytest.raises(RuntimeError):
        await delete_patient(db, patient)
    db.rollback.assert_awaited_once()
