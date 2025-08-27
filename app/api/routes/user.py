# app/api/routes/user.py

from fastapi import APIRouter
from app.models.user import UserModel  # 필요 시
# 다른 의존성 import

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"msg": "pong from user router"}

# 여기에 사용자 관련 API들 추가
