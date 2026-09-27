from google import genai
from app.config import GEMINI_API_KEY

client = genai.Client(
    api_key=GEMINI_API_KEY
)

def generate_story(
    prompt,
    character,
    setting,
    tone,
    art_style
):

    comic_prompt = f"""
You are an expert comic book writer.

Create a 6-panel comic story.

Story idea:
{prompt}

Main character:
{character}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Use exactly this structure:

PANEL 1
Title:
Scene:
Narration:
Dialogue:

PANEL 2
Title:
Scene:
Narration:
Dialogue:

PANEL 3
Title:
Scene:
Narration:
Dialogue:

PANEL 4
Title:
Scene:
Narration:
Dialogue:

PANEL 5
Title:
Scene:
Narration:
Dialogue:

PANEL 6
Title:
Scene:
Narration:
Dialogue:

Requirements:
- Connected story from Panel 1 to Panel 6.
- Keep the main character consistent.
- Keep dialogue short.
- Make scenes visually interesting.
- Match the selected tone and art style.
- Give the story a satisfying ending.
"""

    response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=comic_prompt
    )
    

    return response.text