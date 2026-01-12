from Modules.core import Message, Status
from typing import Any
from QQBot.QQ import QQ
from Images.Images import Image
from AI.chat import AI
import os
import json
import time
import random
import datetime
from queue import Queue
from threading import Thread


class QQBot:
    def __init__(
            self,
            QQ_API_BASE: str,
            AI_MODEL: str = "deepseek-chat",
            AI_API_KEY: str = "sk-0b936cb262ca45718cdfe61352c83038",
            AI_API_BASE: str = "https://api.deepseek.com",
            AI_CHARACTOR: str = "default"
        ) -> None:
        self.image = Image()
        self.qq = QQ(
            QQ_API_BASE=QQ_API_BASE,
        )
        self.ai = AI(
            base_url=AI_API_BASE,
            api_key=AI_API_KEY,
            model=AI_MODEL,
            charactor_mod=AI_CHARACTOR
        )
        self.message_queue: Queue[Message] = Queue()
        self.speak: bool = False

        router_thread: Thread = Thread(target=self.task, daemon=True)
        router_thread.start()


    def run(self, data: dict[Any, Any]) -> None:
        message: Message | None = self.clean(data)
        if message:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(message.send_time))} [{message.sender_name}]: {message.content}")
            self.message_queue.put(message)
        else: return None

    def task(self) -> None:
        while True:
            if not self.message_queue.empty():
                message: Message = self.message_queue.get()
                try:
                    self.router(message)
                except Exception as e:
                    print("处理消息时发生错误: ", str(e))
            else:
                time.sleep(1)

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
        
        elif message.content == "说话":
            self.speak = True
            status: Status = self.qq.postMessage(message.group_id, "已开启AI自动回复功能")
            if status.code != "ok":
                print("发送开启回复状态失败: ", status.message)

        elif message.content == "闭嘴":
            self.speak = False
            status: Status = self.qq.postMessage(message.group_id, "已关闭AI自动回复功能")
            if status.code != "ok":
                print("发送关闭回复状态失败: ", status.message)

        elif message.content.startswith("切换角色 "):
            charactor = message.content[len("切换角色 "):].strip()
            status: Status = self.ai.shift_charactor(charactor)
            if status.code == "ok":
                self.qq.postMessage(message.group_id, status.message)
            else:
                self.qq.postMessage(message.group_id, status.message)

        elif message.content == "角色列表":
            charactors: list[str] = self.ai.get_charactors_list()
            charactor_list: str = "当前可用角色列表:\n" + "\n".join(charactors)
            self.qq.postMessage(message.group_id, charactor_list)

        else:
            if not self.speak:
                return
            respond: Status = self.ai.chat(message.content)
            try:
                data = json.loads(respond.message)
                if data['is_pass']:
                    return
                if int(time.time()) - int(message.send_time) > 5:
                    status: Status = self.qq.postMessage(message.group_id, data['messages'][0] + " ", at=str(message.sender_qq))
                else:
                    status: Status = self.qq.postMessage(message.group_id, data['messages'][0])
                time.sleep(random.randint(2, 7))
                for msg in data['messages'][1:]:
                    status: Status = self.qq.postMessage(message.group_id, msg)
                    time.sleep(random.randint(2, 7))
                if status.code != "ok":
                    print("发送AI回复失败: ", status.message)
                    
                
            except Exception as e:
                print("解析AI回复失败: ", str(e))
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

        ignore: bool = True

        for msg in messages:
            if msg['type'] == 'text':
                message += msg["data"]["text"]

            elif msg['type'] == 'face':
                message += f"[表情:{msg['data']['id']}]"

            elif msg['type'] == 'at':
                if msg['data']['qq'] == str(self.qq.qq_number):
                    ignore = False
                else:
                    message += f"@{self.qq.getQQUserName(int(msg['data']['qq']))}"
                
            elif msg['type'] == 'image':
                message += "[图片消息 " + msg['data']['summary'] + "] 这张图片的描述是: "
                url = msg['data'].get('url', '')
                if msg['data']['summary'] == "[动画表情]":
                    discription = self.ai.get_image_info(url, "这是一个表情包，请简要描述表情包的内容和情绪。")
                else:
                    discription = self.ai.get_image_info(url, "请简要描述这张图片的内容。")
                if discription.code == "ok":
                    message += discription.message
                else:
                    message += "[图片描述获取失败]"
                    print("获取图片描述失败: ", discription.message)
            else:
                message += f"[未知消息类型:{msg['type']}]"

        if ignore and self.speak == False:
            return None
        
        return Message(
            sender_name=data['sender']['nickname'],
            sender_qq=data['sender']['user_id'],
            content=message.strip(),
            group_id=data['group_id'],
            send_time=int(time.time())
        )
    

    def test(self, AI_prompt: str="你好", AI_charactor: str = "default") -> None:
        print("QQBot 测试中...")
        print(f"QQ API 地址: {self.qq.base}")
        print(f"QQ 账号: {self.qq.qq_number} - {self.qq.getQQUserName(self.qq.qq_number)}")
        ai_test: Status = self.ai.test_chat(AI_prompt, AI_charactor)
        if ai_test.code == "ok":
            print("AI 测试成功!")
            print(f"AI 回复: {ai_test.message}")
        else:
            print("AI 测试失败!")
            print(f"错误信息: {ai_test.message}")
            raise Exception("AI 测试失败")
        print("测试完成.")