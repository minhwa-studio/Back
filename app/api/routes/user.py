from fastapi import APIRouter, HTTPException, status, Depends
from app.models.user import UserCreate, UserLogin, TokenResponse, UserPublic
from app.models.user import UserModel
from app.services.auth_service import (
    hash_password, create_access_token,
    authenticate_user, is_duplicate_email
)
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/signup", response_model=UserPublic)
async def signup(user: UserCreate):
    if await is_duplicate_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserModel(
        email=user.email,
        password=hash_password(user.password),
        name=user.name,
        phone=user.phone
    )
    await new_user.create()

    return UserPublic(
        id=str(new_user.id),
        email=new_user.email,
        name=new_user.name,
        phone=new_user.phone,
    )

@router.post("/login", response_model=TokenResponse)
async def login(login_data: UserLogin):
    user = await authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserPublic(
            id=str(user.id),
            email=user.email,
            name=user.name,
            phone=user.phone,
        )
    )


@router.get("/me", response_model=UserPublic)
async def get_my_info(current_user: UserModel = Depends(get_current_user)):
    return current_user
