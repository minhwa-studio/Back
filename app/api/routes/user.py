# app/api/routes/user.py

from fastapi import APIRouter, HTTPException
from app.models.user import UserModel, UserCreate
from app.models.pyobjectid import PyObjectId

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate):
    # 이메일 중복 체크
    existing = await UserModel.find_one(UserModel.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    # 비밀번호 해싱 필요 시 여기 추가 (예: bcrypt)

    new_user = UserModel(
        email=user.email,
        password=user.password,
        name=user.name,
        phone=user.phone
    )
    await new_user.insert()

    return {"message": "회원가입 성공", "user_id": str(new_user.id)}
