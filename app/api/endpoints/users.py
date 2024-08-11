from fastapi import APIRouter, Depends
from models.schema import UserRequest, UserResponse
from database.session import get_db
from database.models import User
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/users")
async def create_user(user: UserRequest, db: AsyncSession = Depends(get_db)):
    new_user = User(
        name=user.name,
        email=user.email,
    )
    try:
        db.add(new_user)
        await db.commit()
        await db.flush()
        
        added_user = await db.execute(
            select(User).where(User.email == new_user.email)
        )
        added_user = added_user.scalar_one_or_none()
        
        if not added_user:
            raise ValueError("User not found after insertion")
        
        logging.info(f"User {added_user.id} added successfully.")
        
        return UserResponse(
            id=added_user.id,
            name=added_user.name,
            email=added_user.email,
            created_at=added_user.created_at
        )
    except Exception as e:
        await db.rollback()
        raise e
    
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        user = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = user.scalar_one_or_none()
        
        if not user:
            raise ValueError("User not found")
        
        logging.info(f"User {user.id} retrieved successfully.")
        
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at
        )
    except Exception as e:
        raise e