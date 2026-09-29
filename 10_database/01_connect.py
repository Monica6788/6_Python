"""
    DB 연동
"""
import oracledb
import pandas as pd

from _db import connect, get_engine, USER, HOST, PORT, NAME, PASSWORD

# connection 객체 반환 -> _db.py의 connect 함수
conn = connect()

# cursor() => Cursor 객체를 반환하는 함수
#   execute(sql) 함수를 통해 쿼리문 실행의 결과를 반환받을 수 있음.

# DML 실행
with conn.cursor() as cur:
    cur.execute("SELECT (SELECT banner FROM v$version WHERE ROWNUM <= 1) AS v, "
                "sys_context('USERENV', 'DB_NAME') AS db FROM dual")

    # 한 행짜리 결과: fetchone / 여러 행 결과: fetchall
    row = cur.fetchone()

print(f"접속: {USER}@{HOST}:{PORT}/{NAME}")
print(f"조회 결과: v = {row[0]} db = {row[1]}")
print()

# DDL 실행
with conn.cursor() as cur:
    # cur.execute("DROP TABLE demo_commit")
    # IF문과 예외 처리를 넣기 위해 PL/SQL (확장형 SQL 프로그래밍 언어)
    """
        BEGIN 
        -- 1. 동적으로 테이블을 삭제(DROP) 시도
        EXECUTE IMMEDIATE 'DROP TABLE demo_commit';
        
        -- 2. 에러(예외)가 발생했을 때 처리
        EXCEPTION 
            WHEN OTHERS THEN 
                -- 만약 에러 코드가 -942(오라클에서 '
                -- 존재하지 않는 테이블을 삭제하려 할 때' 발생하는 에러)가 아니라면, 
                -- 에러를 그대로 위로 던져서(RAISE) 프로그램을 멈춰라.
                IF SQLCODE != -942 THEN 
                    RAISE; 
                END IF; 
        END;
    """
    cur.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE demo_commit';"
                "EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; "
                "END IF; END;")
    cur.execute("CREATE TABLE demo_commit (id NUMBER, memeo VARCHAR2(50))")

# DML 실행 후 커밋 없이 다른 커넥션 객체에서 DML의 결과 확인
c1 = connect()
with c1.cursor() as cur:
    cur.execute("INSERT INTO demo_commit VALUES(1, 'test1')")
    cur.execute("SELECT COUNT(*) FROM demo_commit")
    # 결과 자체가 튜플 형태이므로 첫 번째 데이터만 인덱싱
    print(f"데이터 추가 후 커밋 없이 바로 확인: {cur.fetchone()[0]}")   # 1
c1.close()

c2 = connect()
with c2.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM demo_commit")
    # 결과 자체가 튜플 형태이므로 첫 번째 데이터만 인덱싱
    print(f"새로운 커넥션에서 조회: {cur.fetchone()[0]}")   # 0
"""
    커밋 하지 않고 커넥션을 반납(close)했을 때 오류가 발생되지 않았음
    DML 실행 후에 트랜잭션 관리를 잘 해야 함.
"""
print()

# DML 실행 및 커밋 후 다른 커넥션 객체에서 DML의 결과 확인
c3 = connect()
with c3.cursor() as cur:
    cur.execute("INSERT INTO demo_commit VALUES (2, 'test2')")
c3.commit()     # 명시적 커밋
c3.close()

c4 = connect()
with c4.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM demo_commit")
    print(f"커밋 후 결과 조회: {cur.fetchone()[0]}")
c4.close()
print()

# 파라미터 바인딩
#   executemany(sql, [, , , ]): 동일한 sql을 사용할 때 값만 바꾸어 여러 번 전달
with conn.cursor() as cur:
    cur.execute("BEGIN EXECUTE IMMEDIATE 'DROP TABLE demo_param';"
            "EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; "
            "END IF; END;")
    cur.execute("CREATE TABLE demo_param (code VARCHAR2(10), price NUMBER)")

    cur.executemany(
        # :1, :2는 해당 테이블의 1번째 컬럼, 2번째 컬럼이라는 뜻.
        # (24_000, "G0001") 형태로 넣는다면 sql을 :2, :1 로 적으면 됨.
        "INSERT INTO demo_param VALUES (:1, :2)",
        [("G0001", 24_000), ("G0002", 55_000), ("G0003", 100_000)]
    )
conn.commit()

with conn.cursor() as cur:
    cur.execute(f"SELECT * FROM demo_param WHERE price > :1", (50_000, ))
    print(f"결과: {len(cur.fetchall())} 행")

"""
    파라미터를 한 개만 넘기더라도 튜플로 전달하는 것을 권장
    
    변수가 여러 개인 경우, 문자열을 하나만 전달하게 되면 자동으로 쪼개어 사용함.
"""
print()

# 조회 결과를 컬럼 이름으로 접근
# Cursor의 기본 반환값은 튜플 형태
plain = oracledb.connect(user=USER, password=PASSWORD,
                         dsn=f"{HOST}:{PORT}/{NAME}")

with plain.cursor() as cur:
    cur.execute("SELECT * FROM demo_param WHERE ROWNUM <= 1")
    print(f"기본 커서: {cur.fetchone()}")
plain.close()

# rowfactory: 컬럼 이름으로 데이터 접근
with conn.cursor() as cur:
    cur.execute("SELECT * FROM demo_param WHERE ROWNUM = 1")
    # cur.description 
    # : DB 커서가 최근 실행한 쿼리의 컬럼 메타데이터(정보)를 담고 있는 속성
    # for col in cur.description
    # : 메타데이터 목록에서 컬럼 하나하나를 col이라는 변수명으로 꺼내 오기
    # lower()로 컬럼명을 전부 소문자로 바꾸고, list comprehension 적용
    columns = [col[0].lower() for col in cur.description]
    # rowfactory : DB 커서가 쿼리 실행 후 가져올 때(fetch),
    #              각 행의 데이터를 어떤 형식으로 포장해서 반환할지 지정하는 속성
    # lambda *args: 익명함수 만들기
    # args: DB에서 조회한 한 행의 컬럼 값들을 통째로 받아 튜플 형태로 묶어주는 역할
    # zip(columns, args): 앞서 만든 소문자 컬럼 리스트와 방금 조회한 데이터 args를
    #                     1대1로 나란히 짝지어 주고, dict로 감싸 딕셔너리화
    cur.rowfactory = lambda *args: dict(zip(columns, args))

    print(f"rowfactory 설정 후: {cur.fetchone()}")
print()

# SQLAlchemy 사용 이유? => Pandas와의 연계성
engine = get_engine()

df = pd.read_sql("SELECT * FROM demo_param ORDER BY price DESC", engine)
print(df)
print(df.info())
# 가급적 파이썬에서 sort() 함수를 쓰는 것보다,
# DB에서 정렬 후 데이터를 가져올 것. 그게 더 빠름.
print()

with conn.cursor() as cur:
    for t in ["demo_commit", "demo_param"]:
        cur.execute(f"BEGIN EXECUTE IMMEDIATE 'DROP TABLE {t}'; "
        "EXCEPTION WHEN OTHERS THEN IF SQLCODE != -942 THEN RAISE; "
        "END IF; END;")
conn.close()

print("테이블 정리 완료")

