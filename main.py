from fastapi import FastAPI
import uvicorn
import os
from QQBot.core import QQBot
from typing import Any
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

PORT = int(os.getenv("PORT", 8000)) 

qqbot = QQBot(
    QQ_API_BASE=os.getenv("QQ_API_BASE", ""),
    AI_MODEL=os.getenv("AI_MODEL", ""),
    AI_API_KEY=os.getenv("AI_API_KEY", "sk-xxxxxxxxxxxxxxxxxxxxxx"),
    AI_API_BASE=os.getenv("AI_API_BASE", ""),
    AI_CHARACTOR=os.getenv("AI_CHARACTOR", "")
)


@app.post("/qq")
def receive_qq(payload: dict[Any, Any]):
    qqbot.run(payload)


if __name__ == "__main__":
    qqbot.test()
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)