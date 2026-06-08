import requests, sys, os
sys.path.insert(0, os.path.dirname(__file__))

# 测试上传
url = "http://localhost:8000/api/chat/upload"
files = {"file": ("test.txt", b"hello world", "text/plain")}
r = requests.post(url, files=files)
print(f"上传测试: {r.status_code} {r.json()}")

# 测试带图片的消息
file_id = r.json()["id"]
url2 = "http://localhost:8000/api/chat/conversations"
r2 = requests.post(url2, json={})
conv_id = r2.json()["id"]
print(f"对话: {conv_id}")

# 先发纯文本
r3 = requests.post(f"http://localhost:8000/api/chat/conversations/{conv_id}/messages", json={"content": "你好", "images": []})
print(f"文本消息: {r3.status_code}")
if r3.status_code == 200:
    print(f"  AI: {r3.json()['reply'][:60]}")
else:
    print(f"  {r3.text[:200]}")
