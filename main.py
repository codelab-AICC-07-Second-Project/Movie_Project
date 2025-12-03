from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from routers import auth, movie

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "This is the root page"}