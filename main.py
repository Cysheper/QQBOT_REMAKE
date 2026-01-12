from fastapi import FastAPI
import uvicorn
import os
from QQBot.core import QQBot
from typing import Any

app = FastAPI()

PORT = int(os.getenv("PORT", 8000)) 

qqbot = QQBot(
    QQ_API_BASE="127.0.0.1:3001",
    QQ_NUMBER=3109058878,
    AI_MODEL="deepseek-chat",
    AI_API_KEY="sk-0b936cb262ca45718cdfe61352c83038",
    AI_API_BASE="https://api.deepseek.com",
    AI_CHARACTOR="default"
)

@app.post("/qq")
def receive_qq(payload: dict[Any, Any]):
    qqbot.run(payload)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)