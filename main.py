from fastapi import FastAPI
import uvicorn
import os
from QQBot.core import QQBot
from typing import Any

app = FastAPI()

PORT = int(os.getenv("PORT", 8000)) 

@app.post("/qq")
def receive_qq(payload: dict[Any, Any]):
    qqbot = QQBot()
    qqbot.run(payload)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)