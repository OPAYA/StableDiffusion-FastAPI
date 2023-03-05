from fastapi import APIRouter
from app.services.predict import StabilityService
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()
stability_service = StabilityService(os.environ.get('STABILITY_KEY'))


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
    return {
        "image_urls": await stability_service.generate_image(
            prompt, seed, steps, cfg_scale, width, height, samples
        )
    }
