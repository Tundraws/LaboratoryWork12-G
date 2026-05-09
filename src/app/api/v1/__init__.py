from fastapi import APIRouter

from src.app.api.v1.appointments import router as appointments_router
from src.app.api.v1.auth import router as auth_router
from src.app.api.v1.doctors import router as doctors_router
from src.app.api.v1.medical_records import router as medical_records_router
from src.app.api.v1.patients import router as patients_router
from src.app.api.v1.prescriptions import router as prescriptions_router
from src.app.api.v1.reports import router as reports_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(auth_router)
api_router.include_router(patients_router)
api_router.include_router(doctors_router)
api_router.include_router(appointments_router)
api_router.include_router(prescriptions_router)
api_router.include_router(medical_records_router)
api_router.include_router(reports_router)
