from fastapi import APIRouter
from pydantic import BaseModel
from app.services.predict_service import generate_image

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/predict")
async def predict_image(req: PromptRequest):
    img = await generate_image(req.prompt)
    # 결과 저장 로직 추가 (Mongo에 저장 등)
    return {"message": "image created"}
