# 모델 로딩 (예시, SD3 로컬 inference용 커스텀 코드 필요 시 수정)
import torch
from diffusers import StableDiffusionPipeline

def load_model():
    pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-3", torch_dtype=torch.float16)
    pipe.to("cuda")
    return pipe
