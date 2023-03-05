import os
import io
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation


class StabilityService:
    def __init__(self, key):
        self.stability_api = None

   # async def initialize(self, key):
        os.environ["STABILITY_HOST"] = "grpc.stability.ai:443"
        os.environ["STABILITY_KEY"] = key
        self.stability_api = client.StabilityInference(
            key=key, verbose=True, engine="stable-diffusion-v1-5"
        )

    async def generate_image(
        self,
        prompt: str,
        seed: int = 992446758,
        steps: int = 30,
        cfg_scale: float = 8.0,
        width: int = 512,
        height: int = 512,
        samples: int = 1,
    ):
       # self.initialize(os.environ.get('STABILITY_KEY'))
        
        if self.stability_api is None:
            raise ValueError("Stability API is not initialized. Please call initialize() method first.")
        
        answers = self.stability_api.generate(
            prompt=prompt,
            seed=seed,
            steps=steps,
            cfg_scale=cfg_scale,
            width=width,
            height=height,
            samples=samples,
            sampler=generation.SAMPLER_K_DPMPP_2M,
        )
        images = []
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed. Please modify the prompt and try again."
                    )
                if artifact.type == generation.ARTIFACT_IMAGE:
                    images.append(artifact.binary)
        return images
