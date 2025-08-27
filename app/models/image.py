from pydantic import BaseModel, Field
from typing import Optional
from beanie import Document
from bson import ObjectId
from datetime import datetime
from app.models.pyobjectid import PyObjectId

class ImageModel(Document):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId
    gallery_id: Optional[PyObjectId] = None
    original_img_url: str
    transform_img_url: str
    original_img_name: str
    transform_img_name: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_final: bool = False

    class Settings:
        name = "images"

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat(),
        }
