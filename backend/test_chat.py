import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from app.database import Base, engine
from app.models.chat import *
Base.metadata.create_all(bind=engine)

from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

r = client.post("/api/chat/conversations", json={})
conv_id = r.json()["id"]
print(f"对话ID: {conv_id}")

r = client.post(f"/api/chat/conversations/{conv_id}/messages", json={"content": "你好，请用一句话介绍自己", "images": []})
print(f"状态码: {r.status_code}")
if r.status_code == 200:
    reply = r.json()["reply"]
    print(f"AI回复: {reply[:100]}")
else:
    print(f"错误: {r.text[:300]}")
