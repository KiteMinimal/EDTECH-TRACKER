# crud.py (assignment creation, submission, view logic)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Assignment, Submission, User
from schemas import AssignmentCreate, AssignmentOut, SubmissionCreate, SubmissionOut
from auth import get_current_user

crud_router = APIRouter()

# ========== Teacher creates assignment ==========
@crud_router.post("/assignments", response_model=AssignmentOut)
def create_assignment(
    assignment: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")
    new_assignment = Assignment(
        title=assignment.title,
        description=assignment.description,
        teacher_id=current_user.id
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return new_assignment

# ========== Student submits assignment ==========
@crud_router.post("/submissions", response_model=SubmissionOut)
def submit_assignment(
    submission: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can submit assignments")
    existing_assignment = db.query(Assignment).filter(Assignment.id == submission.assignment_id).first()
    if not existing_assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    new_submission = Submission(
        content=submission.content,
        assignment_id=submission.assignment_id,
        student_id=current_user.id
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return new_submission

# ========== Teacher views submissions ==========
@crud_router.get("/submissions", response_model=list[SubmissionOut])
def view_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view submissions")
    return db.query(Submission).all()