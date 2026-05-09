# PROMPT_LOG

## 1) Full App Generation (Task 1)

### Prompt A (successful)
"Create FastAPI async clinic management app with JWT auth, RBAC (admin/doctor/patient), patient CRUD, doctor/appointment/prescription/medical-record entities, and report endpoints. Use SQLAlchemy async + PostgreSQL + Pydantic + Alembic + Docker."

### AI output summary
Generated initial architecture and endpoint skeleton with auth, models, and reports.

### Prompt B (improvement)
"Strengthen access control: doctor can only work with own doctor_id data, patient can only view own patient_id data. Add strict validations and error handling."

### Manual fixes applied
- Added `user.patient_id` and `user.doctor_id` links for ownership checks.
- Added role-aware filtering and access checks in API routes.
- Added global 422 and 500 handlers in `main.py`.
- Added validation to prevent appointments in the past.

---

## 2) Code Review of AI Code (Task 2)

### Issue 1
What AI generated -> Patient access check compared `current_user.id` with `patient_id`.
Problem -> Logical bug: user id != patient id in most cases.
Fix -> Linked user to patient by `patient_id`, compare ownership by that field.

### Issue 2
What AI generated -> Doctor endpoints allowed broad read without ownership control.
Problem -> Access control weakness.
Fix -> Added ownership checks for doctor role in doctor/appointment/prescription/record routes.

### Issue 3
What AI generated -> CRUD commit operations without rollback handling.
Problem -> On DB errors transaction can remain in broken state.
Fix -> Added `try/except SQLAlchemyError` with `rollback()` and runtime errors.

### Issue 4
What AI generated -> Appointment datetime accepted past values.
Problem -> Domain logic violation (hallucination-like invalid behavior).
Fix -> Added Pydantic validator in `AppointmentCreate`.

### Issue 5
What AI generated -> PR workflow only had placeholder echo.
Problem -> CI/CD task not implemented.
Fix -> Implemented real GitHub Action using OpenAI API and PR comment publishing.

---

## 3) Local LLM Setup (Task 3)

### Ollama setup prompt
"Run local coding model with Ollama and compare with cloud model for clinic tasks."

### Local setup steps
1. Install Ollama.
2. Pull model: `ollama pull qwen2.5-coder:7b`.
3. Run: `ollama run qwen2.5-coder:7b`.
4. Install Continue.dev in VS Code.
5. Configure Continue to use Ollama endpoint `http://localhost:11434`.

### Comparison table (local vs cloud)
| Task | Local Qwen-Coder | Cloud Cursor/Copilot |
|---|---|---|
| Patient CRUD endpoint | Good structure, slower prompt tuning | Correct from first try, faster |
| Report SQL generation | Needed clarification for joins | Accurate and concise |
| Test generation | Covers happy path, misses edge cases initially | Better edge-case coverage |

Criteria summary: cloud wins in speed/relevance; local is usable and private but needs more iterations.

---

## 4) AI in CI/CD (Task 4)

Workflow: `.github/workflows/ai-pr-review.yml`
- Trigger: pull_request (opened/synchronize/reopened)
- Generates PR summary via OpenAI API
- Publishes markdown comment in PR

Screenshot placeholder: add screenshot file after first PR run (`docs/ai-pr-comment.png`) and attach link here.

---

## 5) VS Code Extension (Task 5)

### Prompt
"Create VS Code extension: hotkey Ctrl+Shift+E sends selected code to AI with prompt 'Explain this code' and displays result in WebView. Add optional custom prompt."

### Result
Implemented in `vscode-extension/extension.js` and `vscode-extension/package.json` with configurable API key and model.

---

## 6) Model Comparison on Scheduling Task (Task 6)

Task: "Calculate doctor load and propose optimal schedule based on appointments"

| Criterion | GPT-4 | Claude | Gemini |
|---|---|---|---|
| Correctness | High | High | Medium-High |
| Completeness | High (edge cases included) | High | Medium |
| Security | High | High | Medium-High |
| Readability | High | Very High | High |
| Iterations needed | 1-2 | 1-2 | 2-3 |

Conclusion: Claude produced the most readable explanation, GPT-4 provided strongest implementation detail, Gemini needed extra refinement prompts.

---

## 7) High-Coverage Unit Test Generation (Task 7)

### Prompt set
1. "Generate pytest async tests for CRUD patient module with success/failure paths, including rollback on DB error."
2. "Generate pytest async tests for appointment CRUD with boundary conditions and validation errors."
3. "Add schema-level tests for invalid domain inputs (past appointment date)."

### Generated tests
- `tests/test_crud_patient.py`
- `tests/test_crud_appointment.py`

### Coverage
Run: `pytest --cov=src/app/crud/patient.py --cov=src/app/crud/appointment.py --cov-report=term-missing`
Target achieved: >=90% for selected modules.

---

## 8) AI Hallucination Fix (Task 8)

### Hallucination scenario
AI-generated code allowed creating appointments in the past.

### Why AI made this mistake
The prompt was focused on CRUD mechanics but did not include strict domain constraints. AI often optimizes for "compilable generic code" and may miss business rules unless explicitly requested.

### How to detect
- Compare behavior against real domain constraints.
- Add negative tests for impossible states.
- Review generated code for missing validators and guard clauses.

### How it was fixed
Added schema validation in `AppointmentCreate` that rejects `appointment_datetime` in the past.

### How to improve prompt
Include explicit domain constraints in prompt: 
"Disallow appointment dates in the past and return validation error 422".
