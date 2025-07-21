from pydantic import BaseModel
from typing import Optional

# ========== User Schemas ==========

class UserCreate(BaseModel):
    username: str
    password: str
    role: str  # 'student' or 'teacher'

class UserLogin(BaseModel):
    username: str
    password: str
    role: str  # 'student' or 'teacher'

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

# ========== Assignment Schemas ==========

class AssignmentCreate(BaseModel):
    title: str
    description: str

class AssignmentOut(BaseModel):
    id: int
    title: str
    description: str
    teacher_id: int

    class Config:
        orm_mode = True

# ========== Submission Schemas ==========

class SubmissionCreate(BaseModel):
    assignment_id: int
    content: str

class SubmissionOut(BaseModel):
    id: int
    content: str
    assignment_id: int
    student_id: int
    assignment_title: str
    student_name: str

    class Config:
        orm_mode = True
