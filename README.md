# Clinic Management System

## Student Information
- Full name: Мельникова Анастасия
- Group: 220032-11
- Laboratory work: 12
- Variant: 3(25)

## Program Description
Clinic management system with doctors, patients, appointments, prescriptions, medical records, JWT authentication, role-based access control, and analytical reports.

## Technology Stack
- Python 3.12
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Alembic
- Pytest + HTTPX
- Docker / Docker Compose

## Project Structure
- Source code: `src/`
- Tests: `tests/`

## Build Instructions
1. Create virtual environment
2. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
3. Copy `.env.example` to `.env` and fill values

## Run Instructions
### Local
- Start API: `uvicorn src.app.main:app --reload`
- Open docs: `http://localhost:8000/docs`

### Docker
- Start app and db: `docker compose up --build`

## Usage Examples
### Register
`POST /api/v1/auth/register`
```json
{
  "email": "admin@example.com",
  "password": "StrongPass123",
  "role": "admin"
}
```

### Login
`POST /api/v1/auth/login`
```json
{
  "email": "admin@example.com",
  "password": "StrongPass123"
}
```

### Authorized Request
`GET /api/v1/patients` with header `Authorization: Bearer <token>`
