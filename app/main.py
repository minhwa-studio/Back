from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # ✅ 추가
from app.core.config import settings
from app.db.mongodb import init_db
from app.api.routes import predict, user

app = FastAPI()

# ✅ CORS 설정 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:19006"] 같은 Expo 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def connect_to_mongo():
    await init_db()

# 라우터 등록
app.include_router(predict.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
