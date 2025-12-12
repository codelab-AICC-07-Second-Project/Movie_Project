import pymysql as mysql
from pymysql import IntegrityError
from pymysql.cursors import DictCursor


def read_chart_by_movieId(movieId):
    try:
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='first_scene',
                            cursorclass=DictCursor
                            )
        cursor = con.cursor()
        sql = """
              SELECT rating , count(*) AS count from ratings WHERE movieId = %s
              GROUP BY rating
              ORDER BY rating DESC;"""

        cursor.execute(sql, (movieId,))
        result = cursor.fetchall()


        con.commit();

        con.close();
        print(result);  # insert, update, delete의 결과는 정수값!
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력


    return result;

def read_all(movieId):
    try:
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port=3307,
                            user='root',
                            password='1234',
                            db='first_scene',
                            cursorclass=DictCursor
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "SELECT * FROM reviews WHERE movieId = %s;";

        result = cursor.execute(sql, (movieId,));
        print(result);

        if result >= 1:
            print("데이터 검색 성공!!! ")
        rows = cursor.fetchall(); #전체 목록 다

        print(rows);
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();

    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력

    return rows;


def create(data):
    try :
        # 2. db연결(url(ip+port), id/pw, db명)
        con = mysql.connect(host='localhost',
                            port= 3307,
                            user='root',
                            password='1234',
                            db='first_scene',
                            cursorclass=DictCursor
                            )
        cursor = con.cursor()

        # 3. sql문 작성한 후 sql문을 db서버에 보내자.
        sql = "insert into reviews(accountId, movieId, review_text, result) values (%s, %s, %s, %s)";
        result = cursor.execute(sql, data);
        print(result); # insert, update, delete의 결과는 정수값!
        # 실행된 결과의 행수(레코드 개수)
        if result >= 1 :
            print("데이터 입력 성공!!! ")
        # 4. 보낸 sql문을 바로 실행해줘(반영해줘.)
        con.commit();

        # 5. 커넥션 close
        con.close();
    except IntegrityError as ie:
        print("무결성 에러 발생함.")
        print(ie)  # 에러 정보 출력

if __name__ == '__main__':
    # read_all(150)
    create(['test1',150,'좋아요','긍정'])
