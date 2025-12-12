from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from db.movie_ai_db import get_all_movies, get_user_info_by_id
from services.movie_service import get_recommendations



router = APIRouter(
    prefix='/movielist',
    tags=['movielist']
)
templates = Jinja2Templates(directory='templates')

@router.get('')
# async def show_movie_list(request: Request): --> 주소에 아이디를 노출시키지 않기 위해서 request 객체를 통해 직접 전달.
async def show_movie_list(request: Request, userId: str):
#     아래 주석의 코드에서 request 객체의 형태에 따라 변수를 바꿔야 함
#     user_info = get_user_info_by_id(authId=request.app.status.user_id)
    user_info = await get_user_info_by_id(userId)
    if not user_info:
        return HTMLResponse(f'<h1>{userId} 유저 정보를 찾을 수 없습니다. 다시 로그인해주세요.</h1>')

    movies = await get_all_movies()
    if movies.empty:
        return HTMLResponse("<h1>영화 데이터를 불러올 수 없습니다.</h1>")

    try:
        result = await get_recommendations(movies, user_info)
    except Exception as e:
        print(f'Recommendation error: {e}')
        return HTMLResponse(f'<h1>추천 시스템 오류, {e}</h1>')

    return templates.TemplateResponse('movie.html', {
        'request': request,
        'userId': userId,
        'movies': result
    })

if __name__ == '__main__':
    from unittest.mock import MagicMock
    import asyncio

    async def test():
        print('Server Testing Start')

        mock_request = MagicMock()
        test_user = 'lilymorpho'

        print(f'Testing Recommendation for {test_user}')
        try:
            response = await show_movie_list(mock_request, test_user)

            print(f'Response Status: {response.status_code}')

        except Exception as e:
            print(f'Exception occurred: {e}')

    asyncio.run(test())
