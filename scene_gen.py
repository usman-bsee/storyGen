
negative_prompt = """
((multiple characters, duplicate faces)), low res, deformed
"""


def generate_scene(
        prompts,
        age_prompts,
        face_images,
        age_change,
        character_emphasis='High',
        ip_adapter=None):
    """
    Generates scene images based on prompts, age prompts, and
    face images with different character emphasis levels.

    Args:
        prompts: The prompts to guide the image generation.
        age_prompts: The prompts related to the age of the face images.
        face_images: Face images on which the scenes are generated.
        character_emphasis: Level of emphasis on
                            character ('High', 'Medium', or 'Low').
        controlnet_model: The control net model used for
                            generating age-changing face images.
        ip_adapter: The IP adapter for generating scene images.

    Returns:
        images: The generated scene images based on the input and parameters.
    """

    if character_emphasis == 'High':
        ip_adapter_scale = 0.3

        ip_adapter.set_ip_adapter_scale(ip_adapter_scale)

        images = []
        for i in range(len(face_images)):
            scene_prompt = """Single Face, Single Character.
                                NO deformation in body. """ + prompts[i]
            image = ip_adapter(ip_adapter_image=face_images[i],
                               num_images_per_prompt=1,
                               num_inference_steps=20,
                               seed=2,
                               prompt=scene_prompt,
                               negative_prompt=negative_prompt,
                               width=1024,
                               height=568
                               ).images[0]
            images.append(image)

        return images
