from datetime import date

from pydantic import BaseModel, EmailStr, Field


class UserModel(BaseModel):
    firstname: str = Field("Ivan", min_length=2, max_length=20)
    lastname: str = Field("Ivanov", min_length=2, max_length=30)
    email: EmailStr
    phone_number: str = Field("0501112233", min_length=9, max_length=20)
    birthday: date = Field("1990-08-19")
    additional_data: str


class UserResponse(BaseModel):
    id: int = 1
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        orm_mode = True


class BirthdayResponse(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        orm_mode = True


