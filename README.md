# Student Results API

A FastAPI service for managing subjects, assessments, and student scores. Built as part of the Web Foundations and APIs module.

## Features

- Create and list subjects
- Create and list assessments (tied to a subject)
- Add, update, and retrieve student scores
- Calculate a student's average score across all assessments
- Basic Authentication on all write (POST/PUT) endpoints
- Request validation via Pydantic — malformed or missing fields return clear `422` errors
- Clear `404` errors when referencing a subject, assessment, or student that doesn't exist

## Tech stack

- **FastAPI** — web framework
- **Pydantic** — data validation
- **Uvicorn** — ASGI server
- **Python 3.14**

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/YOUR-USERNAME/student-results-api.git
   cd student-results-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

5. Open the interactive docs:http://127.0.0.1:8000/docs

## Authentication

Write operations (`POST`, `PUT`) require HTTP Basic Auth:

- **Username:** `admin`
- **Password:** `secret123`

> Note: credentials are hardcoded for this learning exercise. In production, this would be replaced with hashed passwords stored securely and token-based auth (e.g. OAuth2/JWT) with expiry, since Basic Auth sends credentials on every request and has no session expiry.

## Endpoints

| Method | Endpoint                          | Auth required | Description                          |
|--------|------------------------------------|----------------|---------------------------------------|
| GET    | `/subjects`                       | No             | List all subjects                     |
| POST   | `/subjects`                       | Yes            | Create a subject                      |
| GET    | `/assessments`                    | No             | List all assessments                  |
| POST   | `/assessments`                    | Yes            | Create an assessment                  |
| POST   | `/scores`                         | Yes            | Add a student's score                 |
| PUT    | `/scores/{score_id}`              | Yes            | Update an existing score              |
| GET    | `/students/{student_id}/results`  | No             | Get all results for a student         |
| GET    | `/students/{student_id}/average`  | No             | Get a student's average score         |

### Example: Create a subject

**Request**
```http
POST /subjects
Authorization: Basic admin:secret123
Content-Type: application/json

{
  "id": 1,
  "name": "Mathematics"
}
```

**Response (200)**
```json
{
  "id": 1,
  "name": "Mathematics"
}
```

### Example: Add a score

**Request**
```http
POST /scores
Authorization: Basic admin:secret123
Content-Type: application/json

{
  "student_id": 101,
  "assessment_id": 1,
  "score": 87
}
```

**Response (200)**
```json
{
  "student_id": 101,
  "assessment_id": 1,
  "score": 87,
  "id": 1
}
```

### Example: Get a student's average

**Request**
```http
GET /students/101/average
```

**Response (200)**
```json
{
  "student_id": 101,
  "average": 87
}
```

## Error handling

- `404 Not Found` — referenced subject, assessment, or student doesn't exist
- `401 Unauthorized` — missing or invalid Basic Auth credentials on a protected endpoint
- `422 Unprocessable Entity` — request body fails validation (e.g. negative score, missing field, wrong type)

## Design notes / tradeoffs

- **In-memory storage**: data is stored in Python dictionaries, not a database. This keeps the project simple for the exercise, but means all data is lost on restart. A production version would use a real database (e.g. PostgreSQL with SQLAlchemy).
- **Basic Auth**: simple to implement and sufficient to demonstrate protecting write endpoints, but weak for production — no token expiry, and credentials are sent on every request. OAuth2 with JWT would be the production-grade alternative.
- **Pydantic validation**: ensures scores can't be negative and all required fields are present before they ever reach the business logic, protecting data integrity.
- **Clear error responses**: distinguishing `401` (auth), `404` (not found), and `422` (bad input) gives API consumers precise, actionable feedback instead of generic failures.

## Testing

A Postman collection (`postman_collection.json`) is included in this repo with sample requests and responses for every endpoint.

## Project structure
student-results-api/
├── main.py # FastAPI app and routes
├── models.py # Pydantic models
├── requirements.txt # Python dependencies
├── postman_collection.json # Exported Postman collection
└── README.md