import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# qwen-plus 模型配置
QWEN_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
QWEN_MODEL = "qwen-plus"

# 读取 API Key
api_key = os.getenv("DASHSCOPE_API_KEY")
client = OpenAI(api_key=api_key, base_url=QWEN_BASE_URL)

# 首页：返回你的 static.index.html 文件
@app.get("/")
def home():
    return FileResponse("static.index.html")

# 聊天接口：固定返回 {"reply": "..."} 格式
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
        return {"reply": "模型调用失败：" + str(e)}
