from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app import schema, database, models, utils

SECRET_KEY = "09d25e06bfb62c5f52b35814cd9d5e06bfb62c5f52b35814cd9d5e06bfb62c5f52b35814cd9d5e06"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 1. Extract Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# 3. Verify token
def verify_access_token(token: str):
    try:
        print(f"🔍 Raw token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"✅ Payload: {payload}")
        id: str = payload.get("user_id")
        if id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return schema.TokenData(id=id)
    except JWTError as e:
        print(f"❌ JWT Error: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


# 4. Get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    token_data = verify_access_token(token)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user