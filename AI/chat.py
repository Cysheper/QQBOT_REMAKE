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
        if not os.path.exists(f"AI/charactors/{charactor_mod}.txt"):
            charactor_mod = "default"

        with open(f"AI/charactors/{charactor_mod}.txt", "r") as f:
            prompt = f.read()
        self.messages: List[ChatCompletionMessageParam] = [{"role": "system", "content": prompt}]


    def chat(self, prompt: str) -> Status:
        try:
            self.messages.append({"role": "user", "content": prompt})
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
        
    def get_image_info(self, image_url: str, prompt: str="") -> Status:
        test_message: List[ChatCompletionMessageParam] = \
            [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": image_url
                        },
                        {
                            "type": "text",
                            "text":  prompt
                        },
                    ],
                }
            ]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=test_message
            )
            reply: str | None = response.choices[0].message.content
            if reply is None:
                reply = ""
            return Status(code="ok", message=reply)
        except Exception as e:
            return Status(code="error", message=f"AI Test Chat Error: {str(e)}")

    def test_chat(self, message: str, charactor: str = "default") -> Status:
        prompt: str = str()
        with open(f"AI/charactors/{charactor}.txt", "r") as f:
            prompt = f.read()
        test_message: List[ChatCompletionMessageParam] = \
            [{"role": "system", "content": prompt}, 
             {"role": "user",   "content": message}]
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=test_message
            )
            reply: str | None = response.choices[0].message.content
            if reply is None:
                reply = ""
            return Status(code="ok", message=reply)
        except Exception as e:
            return Status(code="error", message=f"AI Test Chat Error: {str(e)}")