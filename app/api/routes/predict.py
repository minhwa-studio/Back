from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.models.image import ImageModel
from app.models.pyobjectid import PyObjectId
from datetime import datetime
import uuid

# 추후 Stable Diffusion 모델과 통합 예정
# from app.services.predict_service import generate_image

router = APIRouter()

class PromptRequest(BaseModel):
    user_id: Optional[str] = None  # 유저 연결용


@router.post("/predict")
async def predict_image(req: PromptRequest):
    try:
        uid = str(uuid.uuid4())[:8]

        image_doc = ImageModel(
            user_id=PyObjectId(req.user_id),
            gallery_id=None,
            original_img_url="",
            transform_img_url="",
            original_img_name=f"origin_{uid}.png",
            transform_img_name=f"transform_{uid}.png",
            created_at=datetime.utcnow(),
            is_final=False
        )
        await image_doc.create()

        return {
            "message": "image created",
            "image_id": str(image_doc.id),
            "user_id": req.user_id,
            "created_at": image_doc.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/images")
async def get_images(user_id: str = Query(...)):
    try:
        images = await ImageModel.find((ImageModel.user_id == PyObjectId(user_id)) & (ImageModel.is_final == False)).to_list()
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/art/{user_id}")
async def get_final_images(user_id: str):
    try:
        images = await ImageModel.find((ImageModel.user_id == PyObjectId(user_id)) & (ImageModel.is_final == True)).to_list()
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/images/finalize")
async def finalize_image(image_id: str):
    try:
        image = await ImageModel.get(PyObjectId(image_id))
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.is_final = True
        await image.save()
        return {"message": "Image finalized", "image_id": image_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
