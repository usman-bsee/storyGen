from PIL import Image
import requests
from io import BytesIO
import torch
from transformers import CLIPVisionModelWithProjection
from diffusers import AutoPipelineForText2Image
from diffusers import DPMSolverMultistepScheduler

negative_prompt = """duplicate faces, two faces, ugly face, face with disease,
                    multiple faces, poorly drawn face, fused face, cloned face,
                    extra eyes, oversized eyes, freckles."""


def generate_face_image(prompt, client):
    """
    Generates a realistic picture of a face based on the prompt provided.

    Args:
        prompt (str): The prompt for generating the face image.
        client: The client used for generating the image.
        ip_adapter: The image processing adapter for final image adjustments.

    Returns:
        Image: A realistic picture of a face.
    """

    prompt = str(prompt)
    general_prompt = """You are an agent that generate face
                        images based on the given face description.

    **Instructions:**
    1. The image should be single character image.
    2. The image must have only one face in it.
    3. You must NOT add anything else in the image.
    4. You must exactly follow the given description.
    5. The description will be given in this format. {"face_prompt": "XYZ"}
    XYZ should be replaced by the prompt you'll generate.
    The given description of the character/specie is:
    """

    response = client.images.generate(
        model="dall-e-3",
        prompt=general_prompt + str(prompt),
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img


def initialize_ip_adapter(model_name):
    """
    Initializes an IP adapter pipeline for text-to-image generation.

    Args:
        model_name (str): Name of the model to be used for image generation.

    Returns:
        AutoPipelineForText2Image: Pipeline for image generation.
    """

    image_encoder = CLIPVisionModelWithProjection.from_pretrained(
        "h94/IP-Adapter",
        subfolder="models/image_encoder",
        torch_dtype=torch.float16
    )
    pipeline = AutoPipelineForText2Image.from_pretrained(
        model_name,
        image_encoder=image_encoder,
        torch_dtype=torch.float16
    ).to("cuda")

    # load ip-adapter
    pipeline.load_ip_adapter("h94/IP-Adapter",
                             subfolder="sdxl_models",
                             weight_name="ip-adapter-plus-face_sdxl_vit-h.bin")
    pipeline.scheduler = DPMSolverMultistepScheduler.from_config(
        pipeline.scheduler.config)
    return pipeline
