import asyncio
import aiomysql as mysql
import os

from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db' : os.getenv('DB_NAME')
}

async def get_tmdb_id(movie_id):
    conn = None
    try:
        conn = await mysql.connect(**DB_CONFIG)
        async with conn.cursor(mysql.cursors.DictCursor) as cursor:

            query = "SELECT tmdbId FROM movies WHERE movieId = %s"

            await cursor.execute(query, (movie_id,))
            result = await cursor.fetchone()

            return result

    except Exception as e:
        print(f'DB Error: {e}')
        return None