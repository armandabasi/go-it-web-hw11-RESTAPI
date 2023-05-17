from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_users(limit: int, offset: int, db: Session):
    users = db.query(User).limit(limit).offset(offset).all()
    return users


async def get_user(user_id: int, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    return user


async def get_user_by_email(email: str, db: Session):
    user = db.query(User).filter_by(email=email).first()
    return user


async def get_user_by_phone(phone_number: str, db: Session):
    user = db.query(User).filter_by(phone_number=phone_number).first()
    return user


async def create_user(body: UserModel, db: Session):
    user = User(**body.dict())
    db.add(user)
    db.commit()
    return user


async def update_user(body: UserModel, user_id: int, db: Session):
    user = await get_user(user_id, db)
    if user:
        user.firstname = body.firstname
        user.lastname = body.lastname
        user.email = body.email
        user.phone_number = body.phone_number
        user.birthday = body.birthday
        user.additional_data = body.additional_data
        db.add(user)
        db.commit()
    return user


async def remove_user(user_id: int, db: Session):
    user = await get_user(user_id, db)
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_birthday(days: int, db: Session):
    today = datetime.now().date()
    end_period = today + timedelta(days=days)
    users = db.query(User).all()
    birthday_list = []
    for user in users:
        birthday_this_year = datetime.strptime(user.birthday, "%Y-%m-%d").date().replace(year=2023)
        if end_period >= birthday_this_year >= today:
            birthday_list.append(user)
    return birthday_list


async def search_users(data: str, db: Session):
    users = db.query(User).filter(User.firstname.ilike(f"%{data}%") |
                                  User.lastname.ilike(f"%{data}%") |
                                  User.email.ilike(f"%{data}%")).all()
    return users



