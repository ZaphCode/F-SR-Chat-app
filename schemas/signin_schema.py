from pydantic import BaseModel, EmailStr, Field, ValidationError
from fastapi import Form

class SignInSch(BaseModel):
    email: EmailStr
    password: str = Field(...)

    @classmethod
    def as_form(
        cls,
        email: str = Form(None),
        password: str =  Form(None),
    ):
        try:
            user = cls(email=email, password=password)
            return (user, None)
        except ValidationError as verr:
            errors: dict = {}
            for error in verr.errors():
                errors[error["loc"][0]] = error["msg"]
            return (None, errors)