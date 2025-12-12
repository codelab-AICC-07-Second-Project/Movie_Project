from starlette.responses import RedirectResponse

from db import rating_db as ch
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from models import ai
from models.ai import ai_run

# from main import templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/chart",
    tags=["chart"],
)

@router.get("")
def chart(request: Request):
    # movieId = 150
    movieId = int(request.query_params.get("movieId"))
    userId = request.query_params.get("userId")
    print("====================")
    print("movieId:", movieId)
    # db처리 여기에 넣어서 결과를 가지고 와야해요.
    chart_data = ch.read_chart_by_movieId(movieId)

    print("=====================")
    print(chart_data)


    ###############리뷰코멘트 부분###########

    # db처리 여기에 넣어서 결과를 가지고 와야해요.
    review_data = ch.read_all(movieId)

    print("=====================")
    print(review_data)

    return templates.TemplateResponse("chart.html", {
        "request": request,
        "chart_data": chart_data, "review_data" :review_data,
        "movieId": movieId,
        "userId": userId
    })




@router.get("/review")
def insert(request: Request):
    accountId = request.query_params.get("accountId")
    movieId = int(request.query_params.get("movieId"))
    review_text = request.query_params.get("review_text")
    print("====================")
    print("accountId:", accountId)
    print("movieId:", movieId)
    print("review_text:", review_text)

    ## 리뷰작성하고 나서 서버에서 db에 저장 한 후 차트로 화면호출
    result = ai.ai_run(review_text)
    ch.create([accountId, movieId, review_text, result])


    #############return review_data
    return RedirectResponse(url="/chart?movieId=" + str(movieId) + "&userId=" + accountId, status_code=303)