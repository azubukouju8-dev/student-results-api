from pydantic import BaseModel, Field


class Subject(BaseModel):
    id: int
    name: str


class Assessment(BaseModel):
    id: int
    subject_id: int
    title: str
    max_score: float


class ScoreIn(BaseModel):
    student_id: int
    assessment_id: int
    score: float = Field(ge=0)


class ScoreOut(ScoreIn):
    id: int