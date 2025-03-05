from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password, create_access_token
from app.models.user import User
from pydantic import BaseModel
from authlib.integrations.starlette_client import OAuth
oauth = OAuth()
oauth.register(
    "google",
    client_id="your_google_client_id",
    client_secret="your_google_client_secret",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
)
router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.get("/google-login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(request, redirect_uri="http://localhost:8000/auth/google-callback")

@router.get("/google-callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    return {"message": f"Welcome {user_info['email']}"}


@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):  
    stmt = select(User).where(User.username == request.username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()  # Correct async way to get one record

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}