import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# 跨域（必须加，否则前端连不上）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 通义千问配置
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL = "qwen-turbo"

# 读取 API Key
api_key = os.getenv("DASHSCOPE_API_KEY")
client = OpenAI(api_key=api_key, base_url=QWEN_BASE_URL)

# 首页
@app.get("/")
def home():
    return {"status": "✅ 后端运行正常", "message": "AI聊天服务已启动"}

# 聊天接口
class ChatMessage(BaseModel):
    message: str

@app.post("/chat")
def chat(msg: ChatMessage):
    try:
        completion = client.chat.completions.create(
            model=QWEN_MODEL,
            messages=[{"role": "user", "content": msg.message}]
        )
        return {"reply": completion.choices[0].message.content}
    except Exception as e:
        return {"reply": "服务异常：" + str(e)}
