from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY
import os

client = genai.Client(api_key=GEMINI_API_KEY)


def generate_comic_image(
    scene,
    character,
    setting,
    art_style,
    panel_number
):

    prompt = f"""
Create a single high-quality comic-book illustration.

Panel number:
{panel_number}

Main character:
{character}

Setting:
{setting}

Scene:
{scene}

Art style:
{art_style}

Requirements:
- Keep the character visually consistent.
- Create a clear comic-book composition.
- Show the described scene clearly.
- Detailed environment.
- Dynamic cinematic composition.
- High quality illustration.
- No written text.
- No speech bubbles.
- No captions.
"""

    response = client.models.generate_content(
        model="gemini-3.1-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"]
        )
    )

    os.makedirs("generated/images", exist_ok=True)

    filename = f"generated/images/panel_{panel_number}.png"

    for part in response.parts:

        if part.inline_data is not None:

            image = part.as_image()

            image.save(filename)

            return filename

    return None