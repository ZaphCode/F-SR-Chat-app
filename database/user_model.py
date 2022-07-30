from pydantic import EmailStr, PositiveInt
from redis_om import JsonModel, Field
from typing import Optional
from .connections import redis_db
from datetime import datetime

class User(JsonModel):
    username: str = Field(index=True, full_text_search=True)
    email: EmailStr = Field(index=True, full_text_search=True)
    password: str
    verified: bool = False
    role: str = Field(default="user", index=True)
    image_url: Optional[str] = None
    created_at: datetime = Field(default=datetime.utcnow())
    age: PositiveInt

    class Meta:
        database = redis_db