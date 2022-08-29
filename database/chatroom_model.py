from redis_om import JsonModel, Field
from .connections import get_db
import time

class Chatroom(JsonModel):
    user_pk_1: str = Field(index=True)
    user_pk_2: str = Field(index=True)
    created_at: float = Field(sortable=True, default=time.time())

    class Meta:
        database = get_db()


    