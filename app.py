from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
import openai

app = FastAPI()

# 静态文件（你的网页）
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index():
    return FileResponse("static/index.html")

# ======================
# 原有通用聊天功能（完全不变）
# ======================
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    msg = data.get("message", "")
    
    try:
        client = openai.OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/v1"
        )
        response = client.chat.completions.create(
            model="qwen-turbo",
            messages=[{"role": "user", "content": msg}]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        return {"reply": f"出错：{str(e)}"}

# ======================
# 新增：调用 FastGPT 家电客服
# ======================
@app.post("/chat_service")
async def chat_service(request: Request):
    data = await request.json()
    msg = data.get("message", "")

    base_url = os.getenv("FASTGPT_API_BASE")
    api_key = os.getenv("FASTGPT_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "chatId": "chat_" + os.urandom(8).hex(),
        "stream": False,
        "messages": [{"role": "user", "content": msg}]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=30
            )
        response.raise_for_status()
        result = response.json()
        return {"reply": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"reply": f"客服出错：{str(e)}"}
