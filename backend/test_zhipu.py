import os, httpx, json
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ZHIPU_API_KEY", "")
print(f"Key: {api_key[:8]}...{api_key[-4:]}")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 测试 glm-4v-flash (无图片的纯文本)
payload = {
    "model": "glm-4v-flash",
    "messages": [{"role": "user", "content": "你好"}],
    "temperature": 0.7,
    "max_tokens": 2048
}
r = httpx.post("https://open.bigmodel.cn/api/paas/v4/chat/completions", json=payload, headers=headers, timeout=30)
print(f"glm-4v-flash: {r.status_code}")
if r.status_code == 200:
    print(f"  OK: {r.json()['choices'][0]['message']['content'][:100]}")
else:
    print(f"  Error: {r.text[:200]}")

# 测试 glm-4-flash
payload["model"] = "glm-4-flash"
r = httpx.post("https://open.bigmodel.cn/api/paas/v4/chat/completions", json=payload, headers=headers, timeout=30)
print(f"\nglm-4-flash: {r.status_code}")
if r.status_code == 200:
    print(f"  OK: {r.json()['choices'][0]['message']['content'][:100]}")
else:
    print(f"  Error: {r.text[:200]}")