import os
import joblib
import pandas as pd
import requests
import asyncio
from utils.movie_constants import *
from utils.movie_utils import calculate_age_code, map_gender_to_numerical, map_occupation_id_to_name

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)

MODEL_DIR = os.path.join(PROJECT_DIR, 'models', 'final_optimized_rf_model.joblib')

try:
    MODEL = joblib.load(MODEL_DIR)
    print(f'Model loaded from {MODEL_DIR}')
except Exception as e:
    print(f'Model could not be loaded: {e}')
    MODEL = None

def get_movie_data_from_tmdb(tmdb_id):
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?language=ko-KR'
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {TMDB_API_KEY}'
    }
    response = requests.get(url=url, headers=headers)
    poster_path = response.json()['poster_path']
    localized_title = response.json()['title']
    return poster_path, localized_title

def preprocess_movie_data(movies_df, user_info):
    genre_encoded = movies_df['genres'].str.get_dummies(sep="|")
    movies_prepared =  pd.concat([movies_df, genre_encoded], axis=1)

    age_code = calculate_age_code(user_info['birth'])
    numerical_gender = map_gender_to_numerical(user_info['gender'])
    occupation_name = map_occupation_id_to_name(user_info['occupation'])
    if not occupation_name:
        occupation_name = 'other or not specified'

    for col in USER_COLS:
        movies_prepared[col] = 0

    movies_prepared['gender'] = numerical_gender

    if f'age_{age_code}' in USER_COLS:
        movies_prepared[f'age_{age_code}'] = 1

    if occupation_name in OCCUPATION_NAMES:
        movies_prepared[occupation_name] = 1

    return movies_prepared

async def get_recommendations(movies_df, user_info):
    if MODEL is None:
        return []

    movies_prepared = preprocess_movie_data(movies_df.copy(), user_info)

    X_pred = movies_prepared[ALL_FEATURES]
    movies_prepared['rating'] = MODEL.predict(X_pred)

    recommendations = movies_prepared.sort_values(by=['rating'], ascending=False).head(30)

    movie_list = recommendations[['movieId', 'title', 'rating', 'genres', 'tmdbId']].copy()

    # db에 korean_title과 poster_ing_link가 없으므로 직접 API로 호출
    tasks = [asyncio.to_thread(get_movie_data_from_tmdb, tmdb_id) for tmdb_id in recommendations['tmdbId']]
    tmdb_results = await asyncio.gather(*tasks)

    posters = [res[0] for res in tmdb_results]
    local_titles = [res[1] for res in tmdb_results]

    movie_list['poster_img'] = posters
    movie_list['local_title'] = local_titles

    return movie_list.sample(n=10, weights='rating').to_dict(orient='records')