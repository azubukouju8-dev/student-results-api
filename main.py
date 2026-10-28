import secrets

from fastapi import Depends, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from models import Assessment, ScoreIn, ScoreOut, Subject

app = FastAPI(title="Student Results API")

security = HTTPBasic()

# In-memory "database" — fine for this exercise
subjects: dict[int, Subject] = {}
assessments: dict[int, Assessment] = {}
scores: dict[int, ScoreOut] = {}
score_id_counter = 1


def verify_user(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret123")
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials.username


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid input", "errors": exc.errors()},
    )


# ---------- Subjects ----------

@app.post("/subjects", response_model=Subject)
def create_subject(subject: Subject, user: str = Depends(verify_user)):
    subjects[subject.id] = subject
    return subject


@app.get("/subjects")
def list_subjects():
    return list(subjects.values())


# ---------- Assessments ----------

@app.post("/assessments", response_model=Assessment)
def create_assessment(assessment: Assessment, user: str = Depends(verify_user)):
    if assessment.subject_id not in subjects:
        raise HTTPException(status_code=404, detail="Subject not found")
    assessments[assessment.id] = assessment
    return assessment


@app.get("/assessments")
def list_assessments():
    return list(assessments.values())


# ---------- Scores ----------

@app.post("/scores", response_model=ScoreOut)
def add_score(score: ScoreIn, user: str = Depends(verify_user)):
    global score_id_counter
    if score.assessment_id not in assessments:
        raise HTTPException(status_code=404, detail="Assessment not found")
    new_score = ScoreOut(id=score_id_counter, **score.dict())
    scores[score_id_counter] = new_score
    score_id_counter += 1
    return new_score


@app.put("/scores/{score_id}", response_model=ScoreOut)
def update_score(score_id: int, score: ScoreIn, user: str = Depends(verify_user)):
    if score_id not in scores:
        raise HTTPException(status_code=404, detail="Score not found")
    updated = ScoreOut(id=score_id, **score.dict())
    scores[score_id] = updated
    return updated


@app.get("/students/{student_id}/results")
def get_results(student_id: int):
    results = [s for s in scores.values() if s.student_id == student_id]
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return results


@app.get("/students/{student_id}/average")
def get_average(student_id: int):
    results = [s.score for s in scores.values() if s.student_id == student_id]
    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return {"student_id": student_id, "average": sum(results) / len(results)}