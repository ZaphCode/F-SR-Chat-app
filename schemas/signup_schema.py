from pydantic import BaseModel, EmailStr, Field, PositiveInt, ValidationError, validator
from fastapi import File, Form, UploadFile
from typing import Optional

class SignUpSch(BaseModel):
    username: str = Field(..., max_length=15, min_length=3, example="Paul134")
    email: EmailStr
    age: PositiveInt = Field(..., example=18)
    password: str = Field(..., min_length=8)
    z_file: Optional[UploadFile]

    @validator("z_file")
    def validate_file(cls, file: UploadFile = None):
        accepted_formats = ["image/png", "image/jpg", "image/jpeg"]
        if not file or not file.filename:
            return None
        if file.content_type not in accepted_formats:
            raise ValueError("Invalid File")
        return file

    @classmethod
    def as_form(
        cls,
        username: str = Form(None),
        email: str = Form(None),
        age: int =  Form(None),
        password: str =  Form(None),
        z_file: UploadFile = File(None)
    ):
        try:
            user = cls(username=username, email=email, age=age, password=password, z_file=z_file)
            return (user, None)
        except ValidationError as verr:
            errors: dict = {}
            for error in verr.errors():
                errors[error["loc"][0]] = str(error["msg"]).capitalize()
            return (None, errors)
            