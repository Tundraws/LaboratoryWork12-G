# Clinic Management System

## Student Information
- Full name: ?????????? ?????????
- Group: 220032-11
- Laboratory work: 12
- Variant: 3(25)

## Program Description
??????? ?????????? ???????? ? ?????? ?????????????, ??????? ?? ?????, ?????????, ???????????? ??????? ? ?????????????? ????????.

## Language and Technologies
- Python 3.12
- FastAPI
- SQLAlchemy 2 (async)
- PostgreSQL + asyncpg
- Alembic
- JWT (`python-jose[cryptography]`)
- Password hashing (`passlib[bcrypt]`)
- Pytest + HTTPX + Coverage
- Docker / Docker Compose

## Project Structure
- Source code: `src/`
- Tests: `tests/`

## Build Instructions
1. Create virtual environment and activate it.
2. Install dependencies:
   `pip install -r requirements.txt -r requirements-dev.txt`
3. Copy `.env.example` to `.env` and set variables.

## Run Instructions
### Local
1. Start PostgreSQL (local or Docker).
2. Run API:
   `uvicorn src.app.main:app --reload`
3. Open Swagger: `http://localhost:8000/docs`.

### Docker
1. Start all services:
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

### Authorized request
`GET /api/v1/patients` with `Authorization: Bearer <token>`

## VS Code Extension
`vscode-extension/` contains extension code that explains selected code by hotkey `Ctrl+Shift+E` and renders AI response in WebView.

Install:
1. Open `vscode-extension/` as separate extension project.
2. Run `npm install` and press `F5` in VS Code extension host.
3. Configure setting `clinicCodeExplainer.apiKey`.
