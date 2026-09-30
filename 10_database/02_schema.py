"""
    수집 데이터를 위한 스키마 설계
"""
import pandas as pd

from _db import connect, raw_prices_path, ENCODING

conn = connect()

def drop_table(cur, name):
    """전달된 테이블을 삭제하는 함수"""
    try:
        cur.execute(f"DROP TABLE {name}")
    except Exception as e:
        if  "ORA-00942" not in str(e):
            pass

# =======================================================

# 원본 데이터 저장을 위한 테이블 생성
#   대리키(데이터가 아닌 별도의 키를 추가)를 기본키로 사용
#   => 시퀀스 또는 자동 증가 기본키 (auto increment)
#      oracle 12c버전부터 auto increment 지원
#   - ALWAYS AS: INSERT 시 별도의 값을 지정할 수 없음 
#   - BY DEFAULT AS: 값을 지정하지 않았을 때만 자동 증가

RAW_DDL = """
    CREATE TABLE raw_daily_price (
        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        code VARCHAR2(20),
        "date" VARCHAR2(20),
        open VARCHAR2(20),
        high VARCHAR2(20),
        low VARCHAR2(20),
        close VARCHAR2(20),
        volume VARCHAR2(20),
        "change" VARCHAR2(20),
        "changeRate" VARCHAR2(20),
        -- 수집 시간이나 출처 등 따로 필요한 정보는 자유롭게 추가
        -- CURRENT_TIMESTAMP: SYSDATE의 TIMESTAMP 버전
        collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source VARCHAR2(100)
    )
"""

with conn.cursor() as cur:
    drop_table(cur, "raw_daily_price")
    cur.execute(RAW_DDL)

    print(f"=== raw_daily_price 테이블 생성 완료 ===")
print()
"""
    원본 데이터를 저장할 테이블 생성 시
    - 모든 컬럼의 데이터 타입은 "문자열"로 지정
      (어떤 값이든 저장할 수 있도록 하기 위함!)
    - 제약 조건을 설정하지 않음
    - 수집 시각과 출처도 함께 기록하기 위해 컬럼 추가

    원본 데이터를 저장해야 하는 이유
    - 정제 로직이 잘못된 경우에 대비하기 위함
     (원본 데이터를 따로 저장하지 않았다면 되돌릴 수 없음.)
"""

# keep_default_na
# : 판다스가 파일을 읽어오는 시점에 빈 칸을 결측치(NaN)로 바꾸는 기능
#   False이면 off, True(기본값)이면 on
# raw_prices_path()가 파일이 있으면 파일 경로, 없으면 다운로드 url을 반환
# read_csv()에 다운로드 url을 전달하면 해당 다운로드 파일을 메모리에 올려
# 데이터프레임으로 반환해줌.
raw_sample = pd.read_csv(raw_prices_path(),
                         encoding=ENCODING, dtype=str,
                         keep_default_na=False)
print(raw_sample.head())
print()

bad = raw_sample[raw_sample["close"].isin(["N/A", "-"])].head(2)
good = raw_sample[~raw_sample["close"].isin(["N/A", "-"])].head(2)

# concat: 두 데이터프레임을 합쳐주는 함수.
# 리스트 형태로 good, bad 전달
mix = pd.concat([good, bad])
print(mix[["code", "date", "close"]])
print()

# 제약 조건을 설정한 테이블 추가
with conn.cursor() as cur:
    drop_table(cur, "demo_strict")
    cur.execute("""
        CREATE TABLE demo_strict (
            code VARCHAR2(20),
            "date" DATE,
            close NUMBER NOT NULL
        )
    """)

succ_cnt = 0
# mix의 모든 행을 순회 
# iterrows() 함수는 인덱스와 행 데이터를 같이 반환함
# r에는 현재 반복 중인 한 행의 데이터가 담김
#   (딕셔너리처럼 r['code'] 형태로 접근 가능)
# _는 행 번호(인덱스)를 의미함
#   (첫 번째 자리인 인덱스는 사용 안 할 거라 관례적으로 언더바 사용)
#   (행 데이터만 쓰고 인덱스는 안 쓰겠다는 의미의 언더바!!!)
for _, r in mix.iterrows():
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO demo_strict VALUES"
                " (:1, TO_DATE(:2, 'YYYY-MM-DD'), :3)",
                (r['code'], r['date'], r['close'])
                )
        conn.commit()
        succ_cnt += 1
    except Exception as e:
        conn.rollback()
        print(f"close ({r['close']}) ... {type(e).__name__}")
print(f"데이터 추가 {succ_cnt} / 4 성공")
"""
    close (N/A) ... DatabaseError
    close (N/A) ... DatabaseError
    데이터 추가 2 / 4 성공
"""
print()

# 제약 조건 없이 만든 테이블에 추가
with conn.cursor() as cur:
    cur.executemany(
        'INSERT INTO raw_daily_price (code, "date", close, source)'
        ' VALUES (:1, :2, :3, :4)',
        [ (r['code'], r['date'], r['close'], '실습데이터') 
         for _, r in mix.iterrows() ]
    )
conn.commit()       # 예외처리 생략

with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM raw_daily_price")
    print(f"raw_daily_price 데이터 추가: {cur.fetchone()[0]} / 4 성공")
    # raw_daily_price 데이터 추가: 4 / 4 성공

"""
    원본 테이블은 데이터를 그대로 저장하는 것이 목적임.
    결측과 이상치 등은 정제 단계에서 판단한다.
"""

CLEAN_DDL = """
    CREATE TABLE daily_price (
        id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
        code VARCHAR2(20)   NOT NULL,
        "date" DATE         NOT NULL,
        open NUMBER(20),
        high NUMBER(20),
        low NUMBER(20),
        close NUMBER(20),
        volume NUMBER(20),
        "change" NUMBER(20),
        "changeRate" NUMBER(6, 2),
        -- 수집 시간이나 출처 등 따로 필요한 정보는 자유롭게 추가
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT uk_code_date UNIQUE (code, "date")
    )
"""

with conn.cursor() as cur:
    drop_table(cur, "daily_price")
    cur.execute(CLEAN_DDL)

print("=== daily_price 테이블 생성 완료 ===\n")

"""
    - 금액: 실수 타입 금지 
           (부동 소수점(float)은 오차가 누적될 수 있음. NUMBER 사용)
    - 비율: NUMBER(6, 2): 자릿수 고정. 오차를 줄일 수 있음.
    - 날짜: DATE. 
           (문자열로 저장하게 되면 날짜 계산이나 정렬이 더 어려워질 수 있음.)
    - 코드: VARCHAR2.
           (0부터 시작하는 값인 경우 0을 보존하기 위함.)
"""
# 삭제할 테이블이 늘어날 경우를 위해 리스트 순회 형식으로 테이블 삭제
with conn.cursor() as cur:
    for t in ["demo_strict"]:
        drop_table(cur, t)
conn.close()

print("===== 테이블 정리 완료 =====")