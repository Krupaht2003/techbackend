from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.core.security import hash_password
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    password: str

@router.post("/signup")
async def signup(request: SignupRequest, db: AsyncSession = Depends(get_db)):  
    # Use async select() instead of query()
    stmt = select(User).where(User.username == request.username)
    result = await db.execute(stmt)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    user = User(username=request.username, hashed_password=hash_password(request.password))
    db.add(user)
    await db.commit()  # Use await for async commit
    await db.refresh(user)  # Refresh the instance to update it with the latest data

    return {"message": "User created successfully"}
