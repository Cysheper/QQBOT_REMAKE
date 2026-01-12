from Modules.core import Message, Status
from typing import Any
from QQBot.QQ import QQ
from Images.Images import Image
from AI.chat import AI
import os
import json

class QQBot:
    def __init__(
            self,
            QQ_API_BASE: str,
            QQ_NUMBER: int,
            AI_MODEL: str = "deepseek-chat",
            AI_API_KEY: str = "sk-0b936cb262ca45718cdfe61352c83038",
            AI_API_BASE: str = "https://api.deepseek.com",
            AI_CHARACTOR: str = "default"
        ) -> None:
        self.image = Image()
        self.qq = QQ(
            QQ_API_BASE=QQ_API_BASE,
            QQ_NUMBER=QQ_NUMBER
        )
        self.ai = AI(
            base_url=AI_API_BASE,
            api_key=AI_API_KEY,
            model=AI_MODEL,
            charactor_mod=AI_CHARACTOR
        )


    def run(self, data: dict[Any, Any]) -> None:
        message: Message | None = self.clean(data)
        if message:
            print(f"[{message.sender_name}]: {message.content}")
            self.router(message)


        else: return None

    def router(self, message: Message) -> None:
        if message.content[:2] == "来只":
            repo: str = message.content[2:].strip()
            image_name: str = self.image.getRandomImage(repo).message
            print(f"发送图片: {image_name}")
            url: str = f"https://cynite.oss-cn-guangzhou.aliyuncs.com/QQBot/Image/{image_name}"
            respond: Status = self.qq.postImg(message.group_id, url, willdel=True)
            if respond.code != "ok":
                self.qq.postMessage(message.group_id, respond.message)
            
        elif message.content == "图片详情":
            respond: Status = self.image.getImageList()
            respose : Status = self.qq.postMessage(message.group_id, respond.message)
            if respose.code != "ok":
                print("发送图片列表失败: ", respose.message)
            
        else:
            respond: Status = self.ai.chat(message.content)
            try:
                data = json.loads(respond.message)
                if data['is_pass']:
                    return
                for msg in data['messages']:
                    status: Status = self.qq.postMessage(message.group_id, msg)
                    if status.code != "ok":
                        print("发送AI回复失败: ", status.message)
                
            except Exception as e:
                print("解析AI回复失败: ", e)
                status: Status = self.qq.postMessage(message.group_id, respond.message)


    def clean(self, data: dict[Any, Any]) -> Message | None:
        if 'sender' not in data.keys() or not data['sender']['nickname']:
            return None
        if 'message' not in data.keys() or 'group_id' not in data.keys():
            return None
        
        if isinstance(data['message'], list):
            messages: list[Any] = data['message']
        else: return None

        if data['sender']['user_id'] == self.qq.qq_number:
            return None

        message: str = str()

        for msg in messages:
            if msg['type'] == 'text':
                message += msg["data"]["text"]
            elif msg['type'] == 'face':
                message += f"[表情:{msg['data']['id']}]"
            elif msg['type'] == 'at':
                message += f"@{self.qq.getQQUserName(int(msg['data']['qq']))} "
            elif msg['type'] == 'image':
                message += "[图片]"
            else:
                message += f"[未知消息类型:{msg['type']}]"
        
        return Message(
            sender_name=data['sender']['nickname'],
            content=message,
            group_id=data['group_id']
        )