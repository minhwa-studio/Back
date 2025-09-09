from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query, Request
from fastapi.responses import FileResponse
from typing import Optional, List, Dict, Any
from app.models.image import ImageModel
from app.models.pyobjectid import PyObjectId
from datetime import datetime
import uuid
import aiohttp
import asyncio
import os

router = APIRouter()

# 폴더 생성
os.makedirs("minhwa_img", exist_ok=True)

# 8500 생성 서버 URL
GENERATE_URL = "http://localhost:8500/generate"

# 프롬프트 기본값
PROMPT = (
    "elegant minhwastyle, traditional Korean minhwa painting, hanji paper, "
    "preserve original colors, maintain original color palette, reference original image colors, "
    "refined ink outlines, sophisticated flat colors, artistic folk style, "
    "strong edge definition for human figure, soft hanji paper texture for background, "
    "beautiful portrait painting, graceful human subject, traditional Korean portrait style"
)
NEGATIVE_PROMPT = (
    "photorealistic, 3d render, glossy, high contrast, saturated colors, "
    "western oil painting, anime, manga, ukiyo-e, detailed background, "
    "stamps, seals, red stamps, red seals, ink stamps, "
    "too white, too pale, faded colors, desaturated colors"
)

# 8500 호출 타임아웃 (총 2시간, 연결 60초, 읽기 2시간)
HTTP_TIMEOUT = aiohttp.ClientTimeout(total=7200, sock_connect=60, sock_read=7200)


@router.post("/predict")
async def predict_image(user_id: str = Form(...), file: UploadFile = File(...)):
    """
    1) 업로드 파일 저장 (origin)
    2) 8500 생성 서버로 이미지 + 프롬프트 전송
    3) 응답 이미지 저장 (transform)
    4) DB 기록 후 메타 반환
    """
    try:
        if not user_id:
            raise HTTPException(status_code=400, detail="user_id가 누락되었습니다.")
        if not file:
            raise HTTPException(status_code=400, detail="file이 누락되었습니다.")

        print(f"📥 받은 user_id: {user_id}")

        # origin 이미지 저장
        uid = str(uuid.uuid4())[:8]
        origin_name = f"origin_{uid}.png"
        origin_path = os.path.join("minhwa_img", origin_name)
        with open(origin_path, "wb") as f:
            f.write(await file.read())

        # 8500 서버에 이미지 + prompt 전송
        data = aiohttp.FormData()
        data.add_field("prompt", PROMPT)
        data.add_field("negative_prompt", NEGATIVE_PROMPT)
        # 필요 시 아래 파라미터도 조정/전달 가능
        # data.add_field("num_inference_steps", "12")
        # data.add_field("guidance_scale", "6.5")
        # data.add_field("controlnet_conditioning_scale", "0.8")

        transform_name = f"transform_{uid}.png"
        transform_path = os.path.join("minhwa_img", transform_name)

        async with aiohttp.ClientSession(timeout=HTTP_TIMEOUT) as session:
            with open(origin_path, "rb") as f:
                data.add_field("image", f, filename=origin_name, content_type="image/png")
                try:
                    async with session.post(GENERATE_URL, data=data) as res:
                        if res.status != 200:
                            text = await res.text()
                            raise HTTPException(
                                status_code=500,
                                detail=f"❌ 이미지 생성 실패(8500): {res.status} {text}",
                            )
                        # 변환 이미지 저장
                        with open(transform_path, "wb") as out_file:
                            out_file.write(await res.read())
                except asyncio.TimeoutError:
                    raise HTTPException(status_code=504, detail="❌ 생성 서버 응답 시간 초과(8500)")
                except aiohttp.ClientError as e:
                    raise HTTPException(status_code=502, detail=f"❌ 생성 서버 통신 오류: {e}")

        # DB 저장
        image_doc = ImageModel(
            user_id=PyObjectId(user_id),
            gallery_id=None,
            original_img_url=origin_path,
            transform_img_url=transform_path,
            original_img_name=origin_name,
            transform_img_name=transform_name,
            created_at=datetime.utcnow(),
            is_final=False,
        )
        await image_doc.create()

        return {
            "message": "민화 이미지 생성 성공",
            "image_id": str(image_doc.id),
            "user_id": user_id,
            "origin_img": origin_path,
            "transform_img": transform_path,
            "created_at": image_doc.created_at,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ 예외 발생: {str(e)}")


@router.get("/images")
async def get_images(
    request: Request,
    user_id: str = Query(..., description="사용자 ID"),
    limit: int = Query(50, ge=1, le=200, description="최대 개수(최신순)"),
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
):
    """
    해당 유저의 '변환된 이미지 히스토리' 전체(최신순) 반환.
    여러 번 변환 눌러도 전부 포함.
    프론트는 transform_url을 그대로 <Image source={{ uri }}>에 사용하면 됨.
    """
    try:
        query = (ImageModel.user_id == PyObjectId(user_id))

        images = (
            await ImageModel.find(query)
            .sort(-ImageModel.created_at)
            .skip(skip)
            .limit(limit)
            .to_list()
        )

        base = str(request.base_url).rstrip("/")  # e.g., http://localhost:8000
        result: List[Dict[str, Any]] = []
        for img in images:
            img_id = str(img.id)
            result.append(
                {
                    "image_id": img_id,
                    "created_at": img.created_at,
                    "is_final": img.is_final,
                    "origin_img": img.original_img_url,     # 로컬 경로(디버깅용)
                    "transform_img": img.transform_img_url, # 로컬 경로(디버깅용)
                    "origin_url": f"{base}/image/{img_id}/origin",
                    "transform_url": f"{base}/image/{img_id}/transform",
                }
            )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/art/{user_id}")
async def get_final_images(request: Request, user_id: str):
    """is_final = True 인 확정 이미지를 최신순으로 나열"""
    try:
        images = (
            await ImageModel.find(
                (ImageModel.user_id == PyObjectId(user_id)) & (ImageModel.is_final == True)
            )
            .sort(-ImageModel.created_at)
            .to_list()
        )

        base = str(request.base_url).rstrip("/")
        return [
            {
                "image_id": str(img.id),
                "created_at": img.created_at,
                "transform_url": f"{base}/image/{str(img.id)}/transform",
            }
            for img in images
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/images/finalize")
async def finalize_image(image_id: str):
    """
    이미지 확정 처리(is_final=True)
    """
    try:
        image = await ImageModel.get(PyObjectId(image_id))
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.is_final = True
        await image.save()
        return {"message": "Image finalized", "image_id": image_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------- 이미지 스트리밍 (프론트에서 URI로 직접 표시) --------
@router.get("/image/{image_id}/origin")
async def get_origin_image(image_id: str):
    image = await ImageModel.get(PyObjectId(image_id))
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    path = image.original_img_url
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Original image file not found")
    return FileResponse(path, media_type="image/png", filename=os.path.basename(path))

@router.get("/image/{image_id}/transform")
async def get_transform_image(image_id: str):
    image = await ImageModel.get(PyObjectId(image_id))
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    path = image.transform_img_url
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Transformed image file not found")
    return FileResponse(path, media_type="image/png", filename=os.path.basename(path))

@router.delete("/images/{image_id}")
async def delete_image(image_id: str):
    """
    이미지/파일/레코드 삭제
    """
    try:
        doc = await ImageModel.get(PyObjectId(image_id))
        if not doc:
            raise HTTPException(status_code=404, detail="Image not found")

        # 디스크 파일 삭제 (있으면)
        for path in [doc.original_img_url, doc.transform_img_url]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    # 파일 삭제 실패는 치명적이지 않으니 무시
                    pass

        # DB 레코드 삭제
        await doc.delete()
        return {"message": "deleted", "image_id": image_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))