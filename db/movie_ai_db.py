import asyncio
import os
import aiomysql as mysql
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'db' : os.getenv('DB_NAME')
}

async def get_all_movies():
    conn = None
    try:
        conn = await mysql.connect(**DB_CONFIG)
        async with conn.cursor(mysql.cursors.DictCursor) as cursor:

            query = """
                SELECT movieId, title, genres, tmdbId
                FROM movies
            """

            await cursor.execute(query)
            results = await cursor.fetchall()

            df = pd.DataFrame(results)
            return df

    except Exception as e:
        print(f'DB Error: {e}')
        return pd.DataFrame()

async def get_user_info_by_id(account_id):
    conn = None
    try:
        conn = await mysql.connect(**DB_CONFIG)
        async with conn.cursor(mysql.cursors.DictCursor) as cursor:

            query = "SELECT name, gender, birth, occupation FROM auth WHERE accountId = %s"

            await cursor.execute(query, (account_id,))
            result = await cursor.fetchone()

            return result

    except Exception as e:
        print(f'DB Error: {e}')
        return None

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print("--- Movie Load Test ---")
    movies = loop.run_until_complete(get_all_movies())
    print(movies.head())

    print("--- User Load Test ---")
    user_info = loop.run_until_complete(get_user_info_by_id('lilymorpho'))
    print(user_info)

    loop.close()