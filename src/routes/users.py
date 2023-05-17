from typing import List

from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import UserResponse, UserModel
from src.repository import users as repository_users
router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse])
async def get_users(limit: int = Query(10, le=300), offset: int = 0, db: Session = Depends(get_db)):
    users = await repository_users.get_users(limit, offset, db)
    return users


@router.get("/birthday/", response_model=List[UserResponse])
async def get_users_birthday(days: int = Query(7, le=365),  db: Session = Depends(get_db)):
    users = await repository_users.get_birthday(days, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users


@router.get("/search/", response_model=List[UserResponse])
async def search_users(data: str, db: Session = Depends(get_db)):
    users = await repository_users.search_users(data, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.get_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_users(body: UserModel, db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exist")
    user = await repository_users.get_user_by_phone(body.phone_number, db)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this phone already exist")
    user = await repository_users.create_user(body, db)
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(body: UserModel, user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.update_user(body, user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=UserResponse)
async def remove_user(user_id: int = Path(ge=1), db: Session = Depends(get_db)):
    user = await repository_users.remove_user(user_id, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
