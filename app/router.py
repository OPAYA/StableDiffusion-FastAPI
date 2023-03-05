from fastapi import APIRouter
import io
import zipfile
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
from app.services.predict import StabilityService
import os
import base64
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
stability_service = StabilityService(os.environ.get('STABILITY_KEY'))

def from_image_to_bytes(img):
    """
    pillow image 객체를 bytes로 변환
    """
    # Pillow 이미지 객체를 Bytes로 변환
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format=img.format)
    imgByteArr = imgByteArr.getvalue()
    # Base64로 Bytes를 인코딩
    encoded = base64.b64encode(imgByteArr)
    # Base64로 ascii로 디코딩
    decoded = encoded.decode('ascii')
    return decoded

@router.get("/generate/")
async def generate_image(
    prompt: str,
    seed: int = 992446758,
    steps: int = 30,
    cfg_scale: float = 8.0,
    width: int = 512,
    height: int = 512,
    samples: int = 1,
):
    images = await stability_service.generate_image(
            prompt, seed, steps, cfg_scale, width, height, samples
        )
    img_converted = [from_image_to_bytes(img) for img in images]
    return JSONResponse(img_converted)
   