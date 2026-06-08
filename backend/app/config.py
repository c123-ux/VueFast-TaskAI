import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "个人任务计划管理应用"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
    ZHIPU_API_KEY: str = os.getenv("ZHIPU_API_KEY", "")

settings = Settings()