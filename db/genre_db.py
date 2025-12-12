import pymysql as mysql
from pymysql import IntegrityError
from pymysql.cursors import DictCursor
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db': os.getenv('DB_NAME'),
}


def load_genre_map_from_db():
    print("DB에서 장르 맵 로딩 중...")
    genre_map = {}
    connection = None

    try:
        connection = mysql.connect(**DB_CONFIG, cursorclass=DictCursor)
        cursor = connection.cursor()

        query = "SELECT genreNm, genreNum FROM genres"
        cursor.execute(query)

        # print(cursor.fetchall())

        for dic in cursor.fetchall():
            print("===============")
            print(dic)
            print(dic['genreNm'], dic['genreNum'])
            genre_map[int(dic['genreNum'])] = dic['genreNm']

        print(f"총 {len(genre_map)}개의 장르가 성공적으로 로드되었습니다.")

    except IntegrityError as e:
        print(f"MySQL 오류 발생: {e}")

    finally:
        if connection:
            connection.close()

    return genre_map

GENRE_MAP = load_genre_map_from_db()