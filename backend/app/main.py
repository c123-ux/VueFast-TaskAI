from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from .database import engine, Base
from .routers import tasks, categories, chat
from .config import settings

Base.metadata.create_all(bind=engine)

# 数据库迁移：为现有 conversations 表添加 AI 设置列
inspector = inspect(engine)
existing_cols = [c["name"] for c in inspector.get_columns("conversations")]
with engine.connect() as conn:
    for col, col_type, default in [("ai_role", "VARCHAR", "小美"), ("ai_personality", "VARCHAR", "温柔体贴的妹子"), ("ai_region", "VARCHAR", "广西")]:
        if col not in existing_cols:
            conn.execute(text(f"ALTER TABLE conversations ADD COLUMN {col} {col_type} DEFAULT '{default}'"))
    conn.commit()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix=settings.API_PREFIX, tags=["tasks"])
app.include_router(categories.router, prefix=settings.API_PREFIX, tags=["categories"])
app.include_router(chat.router, prefix=settings.API_PREFIX + "/chat", tags=["chat"])

@app.get("/")
def root():
    return {"message": "个人任务计划管理应用 API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}