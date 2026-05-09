# Clinic Management System

## Student Information
- Full name: ?????????? ?????????
- Group: 220032-11
- Laboratory work: 12
- Variant: 3(25)

## Program Description
??????? ?????????? ???????? ? JWT-???????????????, ??????? ???????? (`admin`, `doctor`, `patient`), CRUD ??? ????????? ???????, ?????????????? ????????, unit-??????? ? ??????????????? ??? AI-??????????????? ??????????.

## Language and Technologies
- Python 3.12
- FastAPI
- SQLAlchemy 2 (async)
- PostgreSQL + asyncpg
- Alembic
- JWT (`python-jose[cryptography]`)
- Password hashing (`passlib[bcrypt]`)
- Pytest + HTTPX + pytest-cov
- Docker / Docker Compose
- GitHub Actions

## Project Structure
- Source code: `src/`
- Tests: `tests/`

## Build Instructions
1. Create virtual environment and activate it.
2. Install dependencies:
   `pip install -r requirements.txt -r requirements-dev.txt`
3. Copy `.env.example` to `.env` and set values.

## Environment Variables
- `APP_NAME`
- `APP_ENV`
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `ACCESS_TOKEN_EXPIRE_MINUTES`

## Run Instructions
### Local
1. Start PostgreSQL (locally or via Docker).
2. Run API:
   `uvicorn src.app.main:app --reload`
3. Open Swagger: `http://localhost:8000/docs`

### Docker
1. Run containers:
   `docker compose up --build`
2. API URL: `http://localhost:8000`

## API Examples
### Register admin
`POST /api/v1/auth/register`
```json
{
  "email": "admin@example.com",
  "password": "StrongPass123",
  "role": "admin"
}
```

### Register doctor user
`POST /api/v1/auth/register`
```json
{
  "email": "doctor@example.com",
  "password": "StrongPass123",
  "role": "doctor",
  "doctor_id": 1
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

### Create patient (admin token required)
`POST /api/v1/patients`
```json
{
  "first_name": "Anna",
  "last_name": "Melnikova",
  "date_of_birth": "2000-01-01",
  "phone": "+375291111111",
  "email": "patient@example.com",
  "address": "Minsk",
  "insurance_policy": "1234567890123456"
}
```

### Reports
- `GET /api/v1/reports/doctors/by-patients-count`
- `GET /api/v1/reports/patients/by-visits`
- `GET /api/v1/reports/prescriptions/by-medication`

## Tests and Coverage
- Run tests: `pytest`
- Run focused coverage for task 7:
  `pytest tests/test_crud_patient.py tests/test_crud_appointment.py --cov=src.app.crud.patient --cov=src.app.crud.appointment --cov-report=term-missing`

## VS Code Extension
Folder `vscode-extension/` contains extension that:
- on `Ctrl+Shift+E` sends selected code to AI with prompt "Explain this code";
- supports optional custom prompt;
- displays response in WebView panel.

Install steps:
1. Open `vscode-extension/` as extension project.
2. Run `npm install`.
3. Press `F5` in VS Code extension host.
4. Set `clinicCodeExplainer.apiKey` in VS Code settings.
