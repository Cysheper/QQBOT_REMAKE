from openai import OpenAI
import os
from typing import List
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from Modules.core import Status

class AI:

    def __init__(
            self, base_url: str, 
            api_key: str, 
            model: str,
            charactor_mod: str = "default",
        ) -> None:
        self.client: OpenAI = OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = model
        if charactor_mod == "default":
            prompt = "You are a helpful assistant."
        else:
            with open(f"AI/charactors/{charactor_mod}.txt", "r") as f:
                prompt = f.read()
        self.messages: List[ChatCompletionMessageParam] = [{"role": "user", "content": prompt}]


    def chat(self, message: str) -> Status:
        try:
            self.messages.append({"role": "user", "content": message})
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )
            reply: str | None = response.choices[0].message.content
            self.messages.append({"role": "assistant", "content": reply})
            if reply is None:
                reply = ""
            print(f"AI: {reply}")
            return Status(code="ok", message=reply)
        except Exception as e:
            return Status(code="error", message=f"AI Chat Error: {str(e)}")