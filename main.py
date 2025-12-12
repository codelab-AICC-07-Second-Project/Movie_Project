from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from db.genre_db import load_genre_map_from_db
from routers import auth_router
# from routers import movie_router
# from routers import tmdb_router
from routers import chart_router

from db.genre_db import GENRE_MAP

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router.router)
# app.include_router(movie_router.router)
# app.include_router(tmdb_router.router)
app.include_router(chart_router.router)

@app.get("/")
def index(request: Request):
        context = {
            "request": request,
            "genre_map": GENRE_MAP
        }
        return templates.TemplateResponse("index.html", context)
