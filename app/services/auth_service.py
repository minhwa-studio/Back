from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.models.user import UserModel
from app.models.pyobjectid import PyObjectId
from app.core.config import settings
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24시간

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_user(email: str, password: str):
    user = await UserModel.find_one(UserModel.email == email)
    if user and verify_password(password, user.password):
        return user
    return None

async def is_duplicate_email(email: str) -> bool:
    user: Optional[UserModel] = await UserModel.find_one(UserModel.email == email)
    return user is not None