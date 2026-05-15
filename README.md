# Clinic Management System

## Student Information
- Full name: Gulyaev Evgeny Aleksandrovich (Гуляев Евгений Александрович)
- Group: 221331
- Laboratory work: 12
- Option type: advanced difficulty (повышенная сложность)
- Variant: 25

## Program Description
Clinic management system with JWT authentication, role-based access control
(`admin`, `doctor`, `patient`), CRUD endpoints for clinic entities, analytics
reports, unit tests, Docker support, AI-assisted PR review workflow, and a
VS Code extension for explaining selected code.

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
2. Apply database migrations:
   `alembic upgrade head`
3. Run API:
   `uvicorn src.app.main:app --reload`
4. Open Swagger: `http://localhost:8000/docs`

### Docker
1. Run containers:
   `docker compose up --build`
2. Docker Compose applies Alembic migrations automatically before starting API.
3. API URL: `http://localhost:8000`

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

Swagger Authorize uses HTTP Bearer auth. Press `Authorize` and paste the JWT
access token from register/login into the `Value` field.

### Create patient (admin token required)
`POST /api/v1/patients`
```json
{
  "first_name": "Anna",
  "last_name": "Gulyaev",
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
- uses DeepSeek chat completions API by default.

Install steps:
1. Open `vscode-extension/` as extension project.
2. Run `npm install`.
3. Press `F5` in VS Code extension host.
4. Set `clinicCodeExplainer.apiKey` to your DeepSeek API key in VS Code settings.
5. Optional: change `clinicCodeExplainer.model` (`deepseek-v4-flash` by default).

## AI PR Review Workflow
The workflow `.github/workflows/ai-pr-review.yml` uses DeepSeek API.
Add repository secret `DEEPSEEK_API_KEY`, then create a pull request or run the
workflow manually from GitHub Actions.
