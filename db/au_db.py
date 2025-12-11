import pymysql as mysql
from pymysql.cursors import DictCursor

DB_CONFIG = {
    "host": "localhost:3307",
    "user": "root",
    "password": "0000",
    "db": "first_scene",
    "charset": "utf8mb4",
    "cursorclass": DictCursor
}

def get_db_connection():
    return mysql.connect(**DB_CONFIG)