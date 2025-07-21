# crud.py (assignment creation, submission, view logic)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Assignment, Submission, User
from schemas import AssignmentCreate, AssignmentOut, SubmissionCreate, SubmissionOut
from auth import get_current_user
from fastapi import Request
from fastapi.responses import JSONResponse


crud_router = APIRouter()

# ========== Teacher creates assignment ==========
@crud_router.post("/assignments", response_model=AssignmentOut)
async def create_assignment(
    assignment: AssignmentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("RAW BODY >>>", await request.body())  # 👈 Logs raw JSON
    print("Parsed assignment:", assignment)
    print("Current user:", current_user.username)
    
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

# ✅ Add this to crud.py
@crud_router.get("/assignments", response_model=list[AssignmentOut])
def get_assignments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Assignment).all()

# ========== Teacher views assignment by ID ==========
@crud_router.get("/assignments/{assignment_id}", response_model=AssignmentOut)
def get_assignment_by_id(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment



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



# ========== Teacher views all submissions ==========
@crud_router.get("/submissions", response_model=list[SubmissionOut])
def view_submissions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view submissions")

    submissions = db.query(Submission).all()
    response = []

    for sub in submissions:
        assignment = db.query(Assignment).filter(Assignment.id == sub.assignment_id).first()
        student = db.query(User).filter(User.id == sub.student_id).first()

        response.append({
            "id": sub.id,
            "content": sub.content,
            "assignment_id": sub.assignment_id,
            "student_id": sub.student_id,
            "assignment_title": assignment.title if assignment else "N/A",
            "student_name": student.username if student else "Unknown"
        })

    return response


@crud_router.delete("/assignments/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id, Assignment.teacher_id == current_user.id).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found or unauthorized")

    db.delete(assignment)
    db.commit()
    return {"message": "Assignment deleted successfully"}

