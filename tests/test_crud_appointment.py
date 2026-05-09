from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest
from sqlalchemy.exc import IntegrityError

from src.app.crud.appointment import create_appointment, delete_appointment, get_appointment, list_appointments
from src.app.models.appointment import Appointment
from src.app.schemas.appointment import AppointmentCreate


@pytest.fixture
def appointment_payload() -> AppointmentCreate:
    return AppointmentCreate(
        patient_id=1,
        doctor_id=2,
        appointment_datetime=datetime.now(timezone.utc) + timedelta(days=1),
        status="scheduled",
        complaint="Headache",
        diagnosis=None,
    )


@pytest.mark.asyncio
async def test_create_appointment_success(appointment_payload: AppointmentCreate) -> None:
    db = SimpleNamespace(add=Mock(), commit=AsyncMock(), rollback=AsyncMock(), refresh=AsyncMock(), delete=AsyncMock())
    result = await create_appointment(db, appointment_payload)
    assert isinstance(result, Appointment)
    db.add.assert_called_once()
    db.commit.assert_awaited_once()
    db.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_appointment_rollback(appointment_payload: AppointmentCreate) -> None:
    db = SimpleNamespace(add=Mock(), commit=AsyncMock(side_effect=IntegrityError("stmt", "params", Exception("x"))), rollback=AsyncMock(), refresh=AsyncMock(), delete=AsyncMock())
    with pytest.raises(RuntimeError):
        await create_appointment(db, appointment_payload)
    db.rollback.assert_awaited_once()


@pytest.mark.asyncio
async def test_list_appointments() -> None:
    db = SimpleNamespace(execute=AsyncMock())
    db.execute.return_value = SimpleNamespace(scalars=lambda: SimpleNamespace(all=lambda: []))
    result = await list_appointments(db)
    assert result == []


@pytest.mark.asyncio
async def test_get_appointment_none() -> None:
    db = SimpleNamespace(execute=AsyncMock())
    db.execute.return_value = SimpleNamespace(scalar_one_or_none=lambda: None)
    result = await get_appointment(db, 10)
    assert result is None


@pytest.mark.asyncio
async def test_delete_appointment_success() -> None:
    db = SimpleNamespace(delete=AsyncMock(), commit=AsyncMock(), rollback=AsyncMock())
    appointment = Appointment(
        id=1,
        patient_id=1,
        doctor_id=2,
        appointment_datetime=datetime.now(),
        status="scheduled",
        complaint="Headache",
        diagnosis=None,
    )
    await delete_appointment(db, appointment)
    db.delete.assert_awaited_once_with(appointment)
    db.commit.assert_awaited_once()


def test_appointment_schema_rejects_past_datetime() -> None:
    with pytest.raises(ValueError):
        AppointmentCreate(
            patient_id=1,
            doctor_id=2,
            appointment_datetime=datetime.now(timezone.utc) - timedelta(days=1),
            status="scheduled",
            complaint="Pain",
            diagnosis=None,
        )


@pytest.mark.asyncio
async def test_delete_appointment_rollback() -> None:
    db = SimpleNamespace(delete=AsyncMock(), commit=AsyncMock(side_effect=IntegrityError("stmt", "params", Exception("x"))), rollback=AsyncMock())
    appointment = Appointment(
        id=1,
        patient_id=1,
        doctor_id=2,
        appointment_datetime=datetime.now(),
        status="scheduled",
        complaint="Headache",
        diagnosis=None,
    )
    with pytest.raises(RuntimeError):
        await delete_appointment(db, appointment)
    db.rollback.assert_awaited_once()
