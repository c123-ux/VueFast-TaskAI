from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models.task import Task as TaskModel, Category as CategoryModel
from ..schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter()

@router.get("/tasks", response_model=List[Task])
def read_tasks(
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[int] = None,
    priority: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TaskModel)
    if status is not None:
        query = query.filter(TaskModel.status == status)
    if priority is not None:
        query = query.filter(TaskModel.priority == priority)
    if category_id is not None:
        query = query.filter(TaskModel.categories.any(CategoryModel.id == category_id))
    
    tasks = query.order_by(TaskModel.priority.desc(), TaskModel.created_at.desc()).offset(skip).limit(limit).all()
    return tasks

@router.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = TaskModel(
        title=task.title,
        description=task.description,
        priority=task.priority,
        status=task.status,
        due_date=task.due_date
    )
    
    if task.category_ids:
        categories = db.query(CategoryModel).filter(CategoryModel.id.in_(task.category_ids)).all()
        db_task.categories = categories
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    update_data = task.model_dump(exclude_unset=True)
    if "category_ids" in update_data:
        category_ids = update_data.pop("category_ids")
        if category_ids is not None:
            categories = db.query(CategoryModel).filter(CategoryModel.id.in_(category_ids)).all()
            db_task.categories = categories
    
    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    db.delete(db_task)
    db.commit()
    return {"message": "任务已删除"}