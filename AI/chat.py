from openai import OpenAI
import os
from typing import List, Iterable
from openai.types.chat import ChatCompletionMessage, ChatCompletionMessageParam
from Modules.core import Status
import json
from database.database import database

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

        self.charactor_mod = charactor_mod

        with open(f"AI/charactors/{charactor_mod}.txt", "r") as f:
            prompt = f.read()

        self.messages: List[ChatCompletionMessageParam] = [{"role": "system", "content": prompt}]
        self.db: database = database("AI/memories")


    def chat(self, prompt: str) -> Status:
        try:
            self.messages.append({"role": "user", "content": prompt})
            self.add_memory({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages
            )

            reply: str | None = response.choices[0].message.content
            if reply is None: reply = ""

            content: ChatCompletionMessageParam = {"role": "assistant", "content": reply}
            self.messages.append(content)
            print(f"AI: {reply}")
            self.add_memory(content)
            return Status(code="ok", message=reply)
        
        except Exception as e:
            return Status(code="error", message=f"AI Chat Error: {str(e)}")
        

    def add_memory(self, message: ChatCompletionMessageParam) -> None:
        try:
            self.db.insert(key=self.charactor_mod, payload=message)
        except Exception as e:
            print(f"Add Memory Error: {str(e)}")

    def shift_charactor(self, charactor: str) -> Status:
        if not os.path.exists(f"AI/charactors/{charactor}.txt"):
            return Status(code="error", message=f"Character '{charactor}' does not exist.")
        with open(f"AI/charactors/{charactor}.txt", "r") as f:
            prompt = f.read()
        self.messages = [{"role": "system", "content": prompt}]
        self.charactor_mod = charactor
        return Status(code="ok", message=f"Character switched to '{charactor}' successfully.")
    

    def get_charactors_list(self) -> List[str]:
        files = os.listdir("AI/charactors")
        charactors = [os.path.splitext(file)[0] for file in files if file.endswith(".txt")]
        return charactors
    
        
    def get_image_info(self, image_url: str, prompt: str="") -> Status:
        test_message : List[ChatCompletionMessageParam]= \
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
                } # type: ignore
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