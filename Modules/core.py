from pydantic import BaseModel


class Message(BaseModel):
    sender_name: str
    content: str
    group_id: int
     

from typing import Literal
StatusCode = Literal["ok", "error"]

class Status(BaseModel):
    code: StatusCode
    message: str

class AI_Response(BaseModel):
    message_list: list[str]

