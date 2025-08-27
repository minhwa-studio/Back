from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from app.models.pyobjectid import PyObjectId

class GalleryModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    art_id: PyObjectId  # 단일 art_id 기준으로 수정
    gallery_title: str
    gallery_content: Optional[str] = None
    starCnt: Optional[int] = 0
    gallery_comment: Optional[str] = None  # 문자열 필드로 단일 코멘트
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }