from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    color: str = "#409EFF"

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 2
    status: int = 0
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    category_ids: List[int] = []

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[int] = None
    due_date: Optional[datetime] = None
    category_ids: Optional[List[int]] = None

class Task(TaskBase):
    id: int
    created_at: datetime
    updated_at: datetime
    categories: List[Category] = []

    class Config:
        from_attributes = True