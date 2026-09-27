from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes import router


app = FastAPI(

    title="ComicCraft",

    description=(
        "AI Comic Story Creator "
        "using Gemini"
    ),

    version="1.0.0"

)


app.mount(

    "/static",

    StaticFiles(
        directory="app/static"
    ),

    name="static"

)


app.mount(

    "/generated",

    StaticFiles(
        directory="generated"
    ),

    name="generated"

)


app.include_router(
    router
)