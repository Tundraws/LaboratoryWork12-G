# PROMPT_LOG

## Task 1. Full Web Application

### Prompt 1 (successful)
"Create an async FastAPI clinic management app on SQLAlchemy + PostgreSQL with JWT auth, RBAC roles admin/doctor/patient, patient CRUD, additional entities (doctor, appointment, prescription, medical record), and report endpoints."

### AI answer summary
Generated initial project skeleton and first implementation of routes/models/schemas/crud.

### Prompt 2 (successful)
"Strengthen permissions so doctor only works with own doctor_id, patient only sees own patient_id data. Add proper 401/403/404/422/500 handling."

### AI answer summary
Proposed ownership checks and role-aware filtering.

### Prompt 3 (successful)
"Add validation and domain rules: forbid past appointments and invalid prescription date ranges."

### AI answer summary
Proposed Pydantic validators and stricter schema constraints.

### Manual edits after AI generation
- Added `user.patient_id` and `user.doctor_id` ownership links.
- Added runtime rollback handling in CRUD modules.
- Added global exception handlers for `422` and `500`.
- Added update endpoints and update CRUD for doctor/appointment/prescription/medical record.
- Improved analytics queries (`outerjoin`, `distinct` for patient counting).

---

## Task 2. Code Review (>=5 issues)

1) What AI generated -> Patient ownership checked by `current_user.id == patient_id`.
Problem -> Logical bug, user id is not equal to patient id by design.
Fix -> Added explicit `patient_id` link in `User` and ownership checks by it.

2) What AI generated -> Doctor had broad read/create flows without strict ownership checks in related entities.
Problem -> Access control vulnerability (horizontal privilege escalation).
Fix -> Added ownership checks for doctor in appointments/prescriptions/medical records for read/write/delete/update.

3) What AI generated -> CRUD commits without `rollback()` on DB exceptions.
Problem -> Broken transaction state and unreliable error propagation.
Fix -> Added `try/except SQLAlchemyError` + rollback + explicit runtime error in CRUD modules.

4) What AI generated -> Appointment datetime accepted past value.
Problem -> Domain violation / hallucination-like invalid business logic.
Fix -> Added validator in appointment schemas to reject past datetime (422).

5) What AI generated -> Alembic migration covered only part of tables.
Problem -> Database schema incomplete for full app and analytics.
Fix -> Extended migration with users/appointments/prescriptions/medical_records tables + indexes and FKs.

6) What AI generated -> Docker image ran as root.
Problem -> Security hardening issue.
Fix -> Added non-root user `appuser` in Dockerfile and switched execution user.

---

## Task 3. Local LLM Setup (Ollama + Continue.dev)

### Prompt used
"Configure local coding LLM for clinic tasks and compare with cloud model on accuracy, speed, relevance."

### Local setup steps
1. Install Ollama.
2. Pull model: `ollama pull qwen2.5-coder:7b`.
3. Run model: `ollama run qwen2.5-coder:7b`.
4. Install Continue.dev in VS Code.
5. Configure Continue provider to `http://localhost:11434`.

### Comparison table
| Task | Local (Qwen-Coder via Ollama) | Cloud (Cursor/Copilot) |
|---|---|---|
| Generate patient CRUD validation | Correct but needed follow-up prompt | Correct on first attempt |
| Build report query for doctor load | Medium quality joins initially | High quality query structure |
| Generate async pytest tests | Good base tests, missed rollback branch first | Better edge-case coverage immediately |

Conclusion: local model is suitable and private, cloud model is faster and usually requires fewer iterations.

---

## Task 4. AI in CI/CD

### Workflow
File: `.github/workflows/ai-pr-review.yml`
- trigger: `pull_request` (opened/synchronize/reopened)
- AI summary generation via DeepSeek API (`DEEPSEEK_API_KEY`)
- auto-comment publish in PR via GitHub API
- graceful fallback comment when DeepSeek quota or network is unavailable

### Required manual proof
Screenshot artifact:
- `docs/ai-pr-comment.jpg`

The workflow was executed successfully. DeepSeek API returned `HTTP 402`
because the account had no available balance, so the workflow generated a
fallback AI review comment instead of failing the CI job. This verifies both the
AI review integration path and the resilient fallback behavior.

---

## Task 5. VS Code Extension

### Prompt
"Create VS Code extension: hotkey Ctrl+Shift+E sends selected code to AI with prompt 'Explain this code', shows result in WebView, optionally allow custom prompt."

### Result
Implemented in `vscode-extension/extension.js` and `vscode-extension/package.json`:
- hotkey `Ctrl+Shift+E`;
- optional custom prompt;
- AI response rendering in WebView;
- configurable DeepSeek API key, endpoint, and model settings.

---

## Task 6. Comparison of 3 AI Models

Complex task: "Implement doctor workload calculation and optimal slot suggestion based on appointments"

| Criterion | GPT-4 | Claude | Gemini |
|---|---|---|---|
| Correctness | High | High | Medium-high |
| Completeness | High | High | Medium |
| Security | High | High | Medium-high |
| Readability | High | Very high | High |
| Iterations needed | 1-2 | 1-2 | 2-3 |

Conclusion: Claude gave most readable explanation, GPT-4 gave strongest implementation detail, Gemini required more refinement prompts.

---

## Task 7. High Coverage Unit Tests

### Prompt set
1. "Generate async pytest tests for `app/crud/patient.py` including success, DB errors, rollback, and edge cases."
2. "Generate async pytest tests for `app/crud/appointment.py` with validation boundaries and rollback handling."
3. "Add tests for invalid domain state (appointment in the past)."

### Generated tests
- `tests/test_crud_patient.py`
- `tests/test_crud_appointment.py`

### Coverage run
Command:
`pytest tests/test_crud_patient.py tests/test_crud_appointment.py --cov=src.app.crud.patient --cov=src.app.crud.appointment --cov-report=term-missing`

Result:
- `src/app/crud/patient.py` -> 100%
- `src/app/crud/appointment.py` -> 100%

---

## Task 8. AI Hallucination Fix + Essay

### Hallucination example
Generated code allowed creating appointment with datetime in the past.

### Why AI made mistake
The initial prompt focused on generic CRUD endpoints but did not explicitly state strict domain constraints. LLM generated syntactically valid but domain-incomplete logic.

### How to detect hallucination in practice
- Check generated code against business rules, not only syntax.
- Add negative tests for impossible states.
- Validate external API/library usage against official docs.

### How it was fixed
Added strict Pydantic validation (`appointment_datetime` must be future) and tests for rejection path.

### How to improve future prompts
Use explicit business constraints in prompt text, for example: 
"Reject appointments in the past with 422 and include tests for this case."
