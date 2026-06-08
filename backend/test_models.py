import os, httpx
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ZHIPU_API_KEY", "")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

models = ["glm-4v", "glm-4v-plus", "glm-4v-flash", "glm-4v-0516", "glm-4-plus", "glm-4v-0414"]
for model in models:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "你好"}],
        "temperature": 0.7,
        "max_tokens": 100
    }
    try:
        r = httpx.post("https://open.bigmodel.cn/api/paas/v4/chat/completions", json=payload, headers=headers, timeout=15)
        if r.status_code == 200:
            reply = r.json()["choices"][0]["message"]["content"]
            print(f"[OK] {model}: {reply[:50]}")
        else:
            err = r.json().get("error", {}).get("code", "")
            print(f"[{r.status_code}] {model}: {err}")
    except Exception as e:
        print(f"[ERR] {model}: {e}")
