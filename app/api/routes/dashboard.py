from fastapi import APIRouter, Depends, HTTPException
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM

router = APIRouter()

async def get_current_user(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/dashboard")
async def dashboard(user: str = Depends(get_current_user)):
    return {"message": f"Welcome {user}, here is your dashboard!"}
