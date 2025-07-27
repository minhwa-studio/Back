from fastapi import FastAPI
from app.core.config import settings

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Server is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=settings.debug)
