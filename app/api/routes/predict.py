from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from app.models.image import ImageModel
from app.models.pyobjectid import PyObjectId
from datetime import datetime
import uuid
import aiohttp
import os
from PIL import Image

router = APIRouter()

# 폴더 생성
os.makedirs("minhwa_img", exist_ok=True)

class PredictRequest(BaseModel):
    user_id: Optional[str] = None

@router.post("/predict")
async def predict_image(user_id: str = Form(...), file: UploadFile = File(...)):
    try:
        print(f"📥 받은 user_id: {user_id}")
        
        # origin 이미지 저장
        uid = str(uuid.uuid4())[:8]
        origin_path = f"minhwa_img/origin_{uid}.png"
        with open(origin_path, "wb") as f:
            f.write(await file.read())

        # 8500 서버에 이미지 + prompt 전송
        generate_url = "http://localhost:8500/generate"
        prompt = (
            "elegant minhwastyle, traditional Korean minhwa painting, hanji paper, "
            "preserve original colors, maintain original color palette, reference original image colors, "
            "refined ink outlines, sophisticated flat colors, artistic folk style, "
            "strong edge definition for human figure, soft hanji paper texture for background, "
            "beautiful portrait painting, graceful human subject, traditional Korean portrait style"
        )
        negative_prompt = (
            "photorealistic, 3d render, glossy, high contrast, saturated colors, "
            "western oil painting, anime, manga, ukiyo-e, detailed background, "
            "stamps, seals, red stamps, red seals, ink stamps, "
            "too white, too pale, faded colors, desaturated colors"
        )

        data = aiohttp.FormData()
        data.add_field("prompt", prompt)
        data.add_field("negative_prompt", negative_prompt)
        data.add_field("image", open(origin_path, "rb"), filename=f"origin_{uid}.png", content_type="image/png")

        async with aiohttp.ClientSession() as session:
            async with session.post(generate_url, data=data) as res:
                if res.status != 200:
                    raise HTTPException(status_code=500, detail="❌ 이미지 생성 실패")
                
                transform_path = f"minhwa_img/transform_{uid}.png"
                with open(transform_path, "wb") as out_file:
                    out_file.write(await res.read())

        # DB 저장
        image_doc = ImageModel(
            user_id=PyObjectId(user_id),
            gallery_id=None,
            original_img_url=origin_path,
            transform_img_url=transform_path,
            original_img_name=f"origin_{uid}.png",
            transform_img_name=f"transform_{uid}.png",
            created_at=datetime.utcnow(),
            is_final=False
        )
        await image_doc.create()

        return {
            "message": "민화 이미지 생성 성공",
            "image_id": str(image_doc.id),
            "user_id": user_id,
            "origin_img": origin_path,
            "transform_img": transform_path,
            "created_at": image_doc.created_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ 예외 발생: {str(e)}")



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
