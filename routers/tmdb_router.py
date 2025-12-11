from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

# from main import templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/chart",
    tags=["chart"],
)

@router.get("")
def chart(request: Request):
    return templates.TemplateResponse("chart.html", {"request": request})