from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles
# from routers import auth_router, movie_router, chart_router tmdb_router


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# app.include_router(auth_router.router)
# app.include_router(movie_router.router)
# app.include_router(chart_router)
# app.include_router(tmdb_router)

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})