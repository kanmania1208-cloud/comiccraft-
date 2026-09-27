from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse, FileResponse
from app.gemini import generate_story
from app.gemini_image import generate_comic_image
from app.pdf_generator import create_pdf

import os
import html
import re

router = APIRouter()


def parse_panels(story):

    panels = []

    pattern = (
        r"\*?\*?PANEL\s+(\d+)\*?\*?"
        r"(.*?)(?=\*?\*?PANEL\s+\d+\*?\*?|$)"
    )

    matches = re.findall(
        pattern,
        story,
        re.DOTALL | re.IGNORECASE
    )

    for number, content in matches:

        content = content.strip()

        title_match = re.search(
            r"\*?\*?Title:\*?\*?\s*(.*)",
            content,
            re.IGNORECASE
        )

        scene_match = re.search(
            r"\*?\*?Scene:\*?\*?\s*(.*)",
            content,
            re.IGNORECASE
        )

        narration_match = re.search(
            r"\*?\*?Narration:\*?\*?\s*(.*)",
            content,
            re.IGNORECASE
        )

        dialogue_match = re.search(
            r"\*?\*?Dialogue:\*?\*?\s*(.*)",
            content,
            re.IGNORECASE | re.DOTALL
        )

        title = (
            title_match.group(1).strip()
            if title_match
            else f"Panel {number}"
        )

        scene = (
            scene_match.group(1).strip()
            if scene_match
            else ""
        )

        narration = (
            narration_match.group(1).strip()
            if narration_match
            else ""
        )

        dialogue = (
            dialogue_match.group(1).strip()
            if dialogue_match
            else ""
        )

        panels.append({
            "number": number,
            "title": title,
            "scene": scene,
            "narration": narration,
            "dialogue": dialogue,
            "image": None
        })

    return panels


@router.get("/", response_class=HTMLResponse)
async def home():

    with open(
        "app/templates/index.html",
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


@router.post(
    "/generate",
    response_class=HTMLResponse
)
async def generate(

    prompt: str = Form(...),

    character: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...)

):

    # Generate story
    story = generate_story(
        prompt,
        character,
        setting,
        tone,
        art_style
    )

    # Create generated folder
    os.makedirs(
        "generated",
        exist_ok=True
    )

    # Save story
    with open(
        "generated/latest_story.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(story)

    # Parse six panels
    panels = parse_panels(story)

    # ------------------------------------------------
    # Generate image ONLY for PANEL 1
    # ------------------------------------------------

    if len(panels) > 0:

        try:

            image_path = generate_comic_image(

                panels[0]["scene"],

                character,

                setting,

                art_style,

                panels[0]["number"]

            )

            panels[0]["image"] = image_path

        except Exception as image_error:

            print(
                "Image generation error:",
                image_error
            )

            panels[0]["image"] = None

    # Create panel cards
    panel_cards = ""

    for panel in panels:

        title = html.escape(
            panel["title"]
        )

        scene = html.escape(
            panel["scene"]
        )

        narration = html.escape(
            panel["narration"]
        )

        dialogue = html.escape(
            panel["dialogue"]
        )

        image_html = ""

        if panel.get("image"):

            image_url = "/" + panel["image"].replace(
                "\\",
                "/"
            )

            image_html = f"""
            <img
                src="{image_url}"
                class="comic-image"
                alt="Comic Panel {panel["number"]}"
            >
            """

        panel_cards += f"""

        <div class="comic-panel">

            <div class="panel-number">
                PANEL {panel["number"]}
            </div>

            {image_html}

            <h3>
                {title}
            </h3>

            <div class="scene-box">

                <span>
                    🎬 Scene
                </span>

                <p>
                    {scene}
                </p>

            </div>

            <div class="narration-box">

                <span>
                    📖 Narration
                </span>

                <p>
                    {narration}
                </p>

            </div>

            <div class="dialogue-box">

                <span>
                    💬 Dialogue
                </span>

                <p>
                    {dialogue}
                </p>

            </div>

        </div>

        """

    # Fallback if parsing fails
    if not panels:

        panel_cards = f"""

        <div class="comic-panel">

            <pre>
{html.escape(story)}
            </pre>

        </div>

        """

    html_content = f"""

    <!DOCTYPE html>

    <html lang="en">

    <head>

        <meta charset="UTF-8">

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <title>
            ComicCraft Result
        </title>

        <link
            rel="stylesheet"
            href="/static/css/style.css"
        >

    </head>

    <body>

        <div class="container">

            <div class="header">

                <h1>
                    🎨 ComicCraft
                </h1>

                <p>
                    Your AI-generated comic story
                </p>

            </div>

            <div class="result">

                <h2>
                    📚 Your 6-Panel Comic
                </h2>

                <div class="comic-grid">

                    {panel_cards}

                </div>

                <div class="result-buttons">

                    <a
                        class="download-btn"
                        href="/download-pdf"
                    >
                        📄 Download PDF
                    </a>

                    <a
                        class="new-btn"
                        href="/"
                    >
                        ✨ Create Another Comic
                    </a>

                </div>

            </div>

        </div>

    </body>

    </html>

    """

    return HTMLResponse(
        content=html_content
    )


@router.get("/download-pdf")
async def download_pdf():

    story_file = (
        "generated/latest_story.txt"
    )

    pdf_file = (
        "generated/comiccraft_comic.pdf"
    )

    if not os.path.exists(
        story_file
    ):

        return HTMLResponse(
            content=(
                "No comic story found. "
                "Please generate a comic first."
            ),
            status_code=404
        )

    with open(
        story_file,
        "r",
        encoding="utf-8"
    ) as file:

        story = file.read()

    create_pdf(
        story,
        pdf_file
    )

    return FileResponse(

        path=pdf_file,

        filename="ComicCraft_Comic.pdf",

        media_type="application/pdf"

    )