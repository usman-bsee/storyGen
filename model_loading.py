import torch
from diffusers import AutoPipelineForText2Image
from diffusers import DDIMScheduler
from diffusers import StableDiffusionPipeline
from transformers import CLIPVisionModelWithProjection


def initialize_ip_adapter(model_name):
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

    pipeline.load_ip_adapter(
        "h94/IP-Adapter",
        subfolder="sdxl_models",
        weight_name="ip-adapter-plus-face_sdxl_vit-h.bin")
    return pipeline


def save_model_locally(model_name, save_directory):
    # Initialize the pipeline
    pipeline = initialize_ip_adapter(model_name)

    # Save the model and necessary components locally
    pipeline.save_pretrained(save_directory)

    # Confirm the model is saved locally
    print(f"Model saved to {save_directory}.")


def load_ip_adapter_from_local(local_directory):
    pipeline = StableDiffusionPipeline.from_pretrained(
        local_directory,
        torch_dtype=torch.float16,
    ).to("cuda")
    pipeline.scheduler = DDIMScheduler.from_config(pipeline.scheduler.config)
    pipeline.load_ip_adapter(
        "h94/IP-Adapter",
        subfolder="models",
        weight_name="ip-adapter-full-face_sd15.bin")
    return pipeline


def check_model_loading(local_directory):
    # Load the model from the local directory
    loaded_pipeline = load_ip_adapter_from_local(local_directory)

    # Confirm the model is loaded from the local directory
    print("Model and pipeline loaded from local directory.", loaded_pipeline)


if __name__ == '__main__':
    model_name = "runwayml/stable-diffusion-v1-5"
    save_directory = "./ip_adapter_model"
    save_model_locally(model_name, save_directory)
    # check_model_loading(save_directory)
