from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, func, Date
from sqlalchemy.orm import declarative_base, validates
from fastapi import HTTPException, status

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)
    birthday = Column(Date)
    additional_data = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        new_phone_number = (
            phone_number.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if new_phone_number.isdigit():
            if len(new_phone_number) == 12:
                return "+" + new_phone_number
            elif len(new_phone_number) == 10 and new_phone_number.startswith("0"):
                return "+38" + new_phone_number
            elif len(new_phone_number) == 11 and new_phone_number.startswith("8"):
                return "+3" + new_phone_number
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number format")

    @validates('birthday')
    def validate_birthday(self, key, birthday):
        today = date.today()
        age = today.year - birthday.year
        if (today.month < birthday.month) or (today.month == birthday.month and today.day < birthday.day):
            age -= 1
        if age < 14:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You must be older 14 years")
