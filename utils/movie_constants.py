import os
from dotenv import load_dotenv

# .env 파일 내용 환경 변수로 로드.
load_dotenv()

# 환경 변수에서 키를 가져옴.
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

TRAINED_GENRES= [
    'Action',
    'Adventure',
    'Animation',
    "Children's",
    'Comedy',
    'Crime',
    'Documentary',
    'Drama',
    'Fantasy',
    'Film-Noir',
    'Horror',
    'Musical',
    'Mystery',
    'Romance',
    'Sci-Fi',
    'Thriller',
    'War',
    'Western',
]
USER_COLS = [
    'gender',
    'age_1',
    'age_18',
    'age_25',
    'age_35',
    'age_45',
    'age_50',
    'age_56',
    'other or not specified',
    'academic/educator',
    'artist',
    'clerical/admin',
    'college/grad student',
    'customer service',
    'doctor/health care',
    'executive/managerial',
    'farmer',
    'homemaker',
    'K-12 student',
    'lawyer',
    'programmer',
    'retired',
    'sales/marketing',
    'scientist',
    'self-employed',
    'technician/engineer',
    'tradesman/craftsman',
    'unemployed',
    'writer'
]

ALL_FEATURES = USER_COLS + TRAINED_GENRES
OCCUPATION_NAMES = USER_COLS[8:]