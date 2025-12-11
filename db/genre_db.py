import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "first_scene",
    "port": 3307
}


def load_genre_map_from_db():
    print("DB에서 장르 맵 로딩 중...")
    genre_map = {}
    connection = None

    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = "SELECT genreNm, genreNum FROM genres"
        cursor.execute(query)

        for (genreNm, genreNum) in cursor:
            genre_map[int(genreNum)] = genreNm

        print(f"총 {len(genre_map)}개의 장르가 성공적으로 로드되었습니다.")

    except mysql.connector.Error as err:
        print(f"MySQL 오류 발생: {err}")

    finally:
        if connection and connection.is_connected():
            connection.close()

    return genre_map

GENRE_MAP = load_genre_map_from_db()