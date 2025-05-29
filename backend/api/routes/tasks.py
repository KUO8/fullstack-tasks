from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from api import models, schemas, database

router = APIRouter(prefix="/api/tasks", tags=["Tasks"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()

    for task in tasks:
        task.title = (
            task.title.split()[0].lower() + 
            ''.join(word.capitalize() for word in task.title.split()[1:])
        )
    return tasks


@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.patch("/{task_id}")
def toggle_task_completed(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.completed = not task.completed
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)