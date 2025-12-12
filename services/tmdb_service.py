import os
import random
import asyncio
import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

HEADERS = {
    'accept': 'application/json',
    'Authorization': f'Bearer {TMDB_API_KEY}'
}

def fetch_data(url):
    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f'Fetch error: {e}')
    return None

def process_movie_data(data):
    if not data:
        return None

    release_data = data.get('release_date', '')
    release = release_data[:4] if release_data else ''

    genre_list = data.get('genres', [])
    genre_data = [g['name'] for g in genre_list] if genre_list else []

    return {
        'tmdb_id': data['id'],
        'title': data['title'],
        'release': release,
        'genres': genre_data,
        'overview': data['overview'],
        'poster_img': data['poster_path'],
        'vote_average': float(data['vote_average'])/2,
        'backdrop_img': data['backdrop_path']
    }

async def get_movie_detail_and_recommendations(tmdb_id: int):
    detail_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?language=ko-KR'
    main_detail = await asyncio.to_thread(fetch_data, detail_url)

    if not main_detail:
        return []

    selected_movie = process_movie_data(main_detail)

    recommend_url = f'https://api.themoviedb.org/3/movie/{tmdb_id}/recommendations?language=ko-KR&page=1'
    recommendations = await asyncio.to_thread(fetch_data, recommend_url)

    recommend_list = recommendations.get('results', []) if recommendations else []

    if len(recommend_list) >= 8:
        recommended_movies = random.sample(recommend_list, 8)
    else:
        recommended_movies = recommend_list

    task = []
    for recommendation in recommended_movies:
        recommend_id = recommendation['id']
        recommend_url = f'https://api.themoviedb.org/3/movie/{recommend_id}?language=ko-KR'

        task.append(asyncio.to_thread(fetch_data, recommend_url))

    recommend_details = await asyncio.gather(*task)

    recommend_result = []
    for recommendation in recommend_details:
        processed = process_movie_data(recommendation)
        if processed:
            recommend_result.append(processed)

    return selected_movie, recommend_result