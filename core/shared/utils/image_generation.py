import base64
import requests
from django.conf import settings
from PIL import Image
from io import BytesIO
import uuid
import os

def generate_image_from_prompt(prompt, style="default"):
    styled_prompt = f"{prompt}, in {style} style" if style != "default" else prompt

    headers = {
        "Authorization": f"Bearer {settings.HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "prompt": styled_prompt,
        "model_name": "SD2"
    }
    response = requests.post(
        "https://router.huggingface.co/hyperbolic/v1/images/generations",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        image_data = response.content
        filename = f"{uuid.uuid4()}.png"
        image_path = os.path.join(settings.MEDIA_ROOT, "story_images", filename)

        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(image_data)

        return f"story_images/{filename}"  # relative path to save in ImageField
    return None
