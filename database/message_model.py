from redis_om import JsonModel, Field
from .connections import redis_db
import time

class Message(JsonModel):
    message: str
    chatroom_pk: str = Field(index=True)
    sender_pk: str = Field(index=True)
    created_at: float = Field(sortable=True, default=time.time())

    class Meta:
        database = redis_db