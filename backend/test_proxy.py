import requests

# 测试前端代理上传链路
url = "http://localhost:5173/api/chat/upload"
with open(__file__, "rb") as f:
    files = {"file": ("test.py", f, "text/plain")}
    r = requests.post(url, files=files)
    print(f"代理上传: {r.status_code}")
    if r.status_code == 200:
        print(f"  OK: {r.json()}")
    else:
        print(f"  Error: {r.text[:200]}")
