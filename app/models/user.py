from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from beanie import Document
from bson import ObjectId
from datetime import datetime
from app.models.pyobjectid import PyObjectId

# ✅ MongoDB 저장 모델 (Beanie Document)
class UserModel(Document):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    password: str
    name: str
    phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        }

# ✅ 회원가입 요청용 모델
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: Optional[str] = None

# ✅ 로그인 요청용 모델
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ✅ 로그인 응답용 모델
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# ✅ 사용자 정보 응답 모델 (id 포함!)
class UserPublic(BaseModel):
    id: str
    email: EmailStr
    name: str
    phone: Optional[str] = None
