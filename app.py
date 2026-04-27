import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# 跨域解决（必加，否则前端报网络错误）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模型配置（qwen-plus）
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_CHAT_MODEL = "qwen-plus"

# 读取环境变量
api_key = os.getenv("DASHSCOPE_API_KEY")
if not api_key:
    raise RuntimeError("⚠️ 未配置环境变量 DASHSCOPE_API_KEY")

client = OpenAI(api_key=api_key, base_url=QWEN_BASE_URL)

# 首页
@app.get("/")
def home():
    return FileResponse("static/index.html")

# 聊天接口
class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
def chat(msg: ChatMessage):
    try:
        completion = client.chat.completions.create(
            model=QWEN_CHAT_MODEL,
            messages=[{"role": "user", "content": msg.message}]
        )
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        print("错误：", str(e))
        return {"reply": f"模型调用失败：{str(e)}"}

# 启动
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
