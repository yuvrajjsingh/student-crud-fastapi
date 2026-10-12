# Students Database CRUD Application

**Internship assignment:** Python Backend Development — EWB Edu Tech Pvt. Ltd.

A student-record management REST API built with **Python, FastAPI, and SQLite**. It supports all mandatory CRUD operations, field validation, filtering, pagination, automatic API documentation, tests, and an optional local Ollama AI endpoint.

## Features

- Create, list, view, replace, partially update, and delete student records.
- SQLite persistence: records remain saved after the server stops.
- Fields: unique auto-generated student ID, name, date of birth, email and/or phone, course, address, enrollment date, creation time, and update time.
- Validation: proper date formats, no future date of birth, email validation, name checks, and at least one contact method.
- Filters: partial name and course match, date-of-birth range, pagination (`skip` and `limit`).
- Clear `404` responses for missing records and `422` responses for invalid input.
- Interactive Swagger API documentation at `/docs`.
- Optional `/ai/ask` endpoint for questions using a local Ollama model; the model does not execute SQL.
- Automated API tests using a temporary test database.

## Requirements

- Python 3.10 or newer (Python 3.11 recommended)
- Internet access for installing Python packages
- Optional only for AI: [Ollama](https://ollama.com/) and a locally downloaded model such as `llama3.2:1b`

## Run locally (Windows PowerShell)

Fastest option: double-click `start_windows.bat`. It creates a virtual environment, installs requirements, and starts the API. Keep its terminal window open.

Or open PowerShell in this project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

If PowerShell blocks activation, you can skip activation and run the virtual environment executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Run locally (macOS / Linux)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: http://127.0.0.1:8000/health

The SQLite database (`students.db`) is created automatically in the project directory. Do not commit a database containing real personal information.

## Quick demo with fictional data

In a second terminal, activate the virtual environment, then run:

```bash
python seed_data.py
```

This inserts three fictional sample students only when the database is empty. It never overwrites existing records.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/students` | Create a student |
| `GET` | `/students` | List and filter students |
| `GET` | `/students/{student_id}` | Get one student |
| `PUT` | `/students/{student_id}` | Replace a student's details |
| `PATCH` | `/students/{student_id}` | Update only supplied fields |
| `DELETE` | `/students/{student_id}` | Delete a student |
| `POST` | `/ai/ask` | Optional local AI question answering |

### Example: create a student

`POST /students` with JSON body:

```json
{
  "name": "Aarav Sharma",
  "date_of_birth": "2005-08-17",
  "email": "aarav@example.com",
  "phone": "9876543210",
  "course": "B.Tech CSE",
  "address": "Lucknow, Uttar Pradesh",
  "enrollment_date": "2024-08-01"
}
```

A successful creation returns HTTP `201 Created` and the generated `id` with timestamps.

### Example: list and filter

```text
GET /students
GET /students?name=aarav
GET /students?course=B.Tech
GET /students?dob_after=2005-01-01&dob_before=2007-01-01
GET /students?skip=0&limit=20
```

Date filters are exclusive: `dob_after=2005-01-01` returns dates strictly after January 1, 2005.

### Example: partial update

`PATCH /students/1`

```json
{
  "course": "M.Tech CSE"
}
```

Only provided fields change. `PUT` requires a full valid student object.

### Example: delete

`DELETE /students/1` returns HTTP `204 No Content` when successful. A non-existent ID returns `404 Not Found`.

## Optional Ollama AI extension

The CRUD API works without Ollama. The `/ai/ask` endpoint answers student-count questions directly from SQLite and can send a bounded set of retrieved student fields to a local Ollama model for other questions. The prompt instructs the model to use only those records and not to execute SQL.

1. Install and start Ollama from https://ollama.com/.
2. Pull the example model:

   ```bash
   ollama pull llama3.2:1b
   ```

3. If needed, configure environment variables before starting the API:

   **PowerShell**
   ```powershell
   $env:OLLAMA_MODEL = "llama3.2:1b"
   $env:OLLAMA_URL = "http://localhost:11434"
   uvicorn app.main:app --reload
   ```

   **macOS / Linux**
   ```bash
   export OLLAMA_MODEL="llama3.2:1b"
   export OLLAMA_URL="http://localhost:11434"
   uvicorn app.main:app --reload
   ```

4. Send `POST /ai/ask`:

   ```json
   { "question": "How many students are there?" }
   ```

   Or ask: `List students born after 2005.`

The count question does not need Ollama. Other AI questions return a clear `503` response if Ollama is unavailable. Use fictional sample data for demos and never send real student personal data to an external model.

## Run automated tests

Install dependencies, then run:

```bash
python -m pytest -v
```

On Windows, you can also double-click `test_windows.bat` after running `start_windows.bat` once to install dependencies.

The tests use a temporary database and cover health check, create/read, filtering, PUT/PATCH, delete, missing IDs, invalid contact data, future birth dates, and a database-grounded count query.

## Suggested GitHub submission steps

Create an empty repository on GitHub, then run these commands inside this project folder:

```bash
git init
git add .
git commit -m "Build student CRUD API with FastAPI and SQLite"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the remote URL with your own GitHub repository URL. Keep `students.db`, secrets, and real student records out of GitHub. Submit the repository link through the channel specified by your trainer.

## Project structure

```text
student-crud-fastapi/
├── app/
│   ├── __init__.py
│   ├── database.py      # SQLite connection and schema
│   ├── main.py          # FastAPI routes and CRUD logic
│   └── schemas.py       # Request validation and response models
├── tests/
│   └── test_api.py      # Automated API tests
├── .gitignore
├── start_windows.bat  # Windows setup + launch helper
├── test_windows.bat   # Windows test helper
├── README.md
├── requirements.txt
└── seed_data.py         # Optional fictional demo data
```

## How to explain the project in a review

1. FastAPI exposes REST endpoints and automatically generates Swagger documentation.
2. Pydantic validates request bodies and query parameters.
3. SQLite stores student records persistently; parameterized SQL queries are used for database operations.
4. Each student receives an auto-incrementing unique ID.
5. HTTP status codes communicate success, invalid input, and missing records.
6. Tests use a separate temporary SQLite database so they do not alter demo or real records.
7. The AI extension is optional and Ollama runs locally; the model receives retrieved data as context and never runs unrestricted SQL.
