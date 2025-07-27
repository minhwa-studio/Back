from app.core.model_loader import load_model

model = load_model()

async def generate_image(prompt: str):
    result = model(prompt).images[0]
    # 파일 저장 or base64 변환
    return result
