# app/main.py
from fastapi import FastAPI
from app.core.config import settings
from app.db.mongodb import init_db
from app.api.routes import predict, user

app = FastAPI()

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
