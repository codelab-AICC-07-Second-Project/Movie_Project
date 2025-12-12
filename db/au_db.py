###
import pymysql
from pymysql.cursors import DictCursor
from pymysql.err import IntegrityError
import bcrypt

import os
from dotenv import load_dotenv
load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST'),
        port=int(os.getenv('DB_PORT')),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        db=os.getenv('DB_NAME'),
        charset='utf8',
        cursorclass=DictCursor
    )


# 회원정보 조회 (로그인에서 사용)
def get_user(accountId):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT * FROM auth WHERE accountId = %s"
    cursor.execute(sql, (accountId,))
    result = cursor.fetchone()

    conn.close()
    return result


# 회원가입하면 INSERT
def insert_user(accountId, password, name, gender, birth, occupation):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO auth (accountId, password, name, gender, birth, occupation)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    cursor.execute(sql, (accountId, password, name, gender, birth, occupation))
    conn.commit()
    conn.close()

# ====================================
#           유저 정보 조회 화면
# ====================================

#유저조회(read_one)
def read_one(accountId):
    try:
        con = get_connection()
        cursor = con.cursor()

        sql = "SELECT * FROM auth WHERE accountId = %s"
        result = cursor.execute(sql, (accountId,))
        print("검색된 행 수:", result)

        row = cursor.fetchone()
        print("검색 결과:", row)
        con.close()

        return row

    except IntegrityError as ie:
        print("DB 에러:", ie)
        return None

#  정보 수정이뮤
def update_user(accountId, password, name, gender, birth, occupation):
    try:
        con = get_connection()
        cursor = con.cursor()

        if not password:
            sql = """
                UPDATE auth
                SET name=%s, gender=%s, birth=%s, occupation=%s
                WHERE accountId=%s
            """
            cursor.execute(sql, (name, gender, birth, occupation, accountId))
        else:

            sql = """
                UPDATE auth
                SET password=%s, name=%s, gender=%s, birth=%s, occupation=%s
                WHERE accountId=%s
            """
            cursor.execute(sql, (password, name, gender, birth, occupation, accountId))

        con.commit()
        con.close()

    except IntegrityError as ie:
        print("무결성 에러:", ie)



# #회원 삭제 (delete)
# def delete_user(accountId):
#     try:
#         con = get_connection()
#         cursor = con.cursor()
#
#         sql = "DELETE FROM auth WHERE accountId = %s"
#
#         result = cursor.execute(sql, (accountId,))
#         print("delete 결과:", result)
#
#         con.commit()
#         con.close()
#
#     except IntegrityError as ie:
#         print("무결성 에러:", ie)
