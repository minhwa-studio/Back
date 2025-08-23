from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


# ObjectId를 Pydantic에서 사용 가능하도록 설정
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# DB 저장용 모델
class UserModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    password: str
    name: str
    phone: Optional[str]
    gallery_ids: List[PyObjectId] = []  # 사용자가 소유한 gallery ID 목록
    art_ids: List[PyObjectId] = []      # 사용자가 소유한 art ID 목록
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }
