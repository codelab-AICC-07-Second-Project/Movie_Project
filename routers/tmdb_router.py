from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from db.tmdb_db import get_tmdb_id
from services.tmdb_service import get_movie_detail_and_recommendations

router = APIRouter(
    prefix='/recommend',
    tags=['recommend']
)
templates = Jinja2Templates(directory='templates')

@router.get('')
async def recommend(request: Request, movieId: int, userId: str):
    movie_data = await get_tmdb_id(movieId)
    if not(movie_data):
        return HTMLResponse(f'<h1>영화 ID({movieId})를 찾을 수 없습니다.</h1>')
    tmdb_id = movie_data['tmdbId']

    selected_movie, recommendations = await get_movie_detail_and_recommendations(tmdb_id)

    if not selected_movie:
        return HTMLResponse('<h1>TMDB에서 영화 정보를 찾을 수 없습니다.</h1>')

    return templates.TemplateResponse('tmdb.html', {
        'request': request,
        'userId' : userId,
        'selected_movie' : selected_movie,
        'recommendations': recommendations
    })
