"""
    대량 적재
"""
import time
import pandas as pd
from _db import connect, get_engine, prices_path, ENCODING

SAMPLE = 1_000
TOTAL = 90_000

conn = connect()
engine = get_engine()

df = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=["date"])
# df(원본)에서 SAMPLE개만큼만 떼어다가 복사본 만들기
sample = df.head(SAMPLE).copy()

cols = ["code", "date", "open", "high", "low", "close", "volume", "change", "changeRate"]
sample = sample[cols]

def reset_table():
    """테이블을 비워주는 함수"""
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE daily_price")

def count_rows():
    """테이블의 행 개수를 반환하는 함수"""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM daily_price")
        return cur.fetchone()[0]

INSERT_SQL = f"""
    INSERT INTO daily_price 
    (code, "date", open, high, low, close, volume, "change", "changeRate")
    VALUES ({','.join( [':%d' % i for i in range(1, 10)] ) })
"""
# 리스트 [':%d' % i for i in range(1, 10)]가 의미하는 것
# [:1, :2, :3, ..., :9]
# ','.join( [':%d' % i for i in range(1, 10)] )
# 각각의 원소들(:1과 :2 등) 사이를 콤마','로 연결해줌.

# itertuples() : 행 단위로 데이터를 가져옴. 속도가 좀 더 빠르다.
rows = [tuple(r) for r in sample.itertuples(index=False)]

# -------------------------------------------------------------------------
# 적재 방식
results = []

# 1. execute 반복 : 한 행씩 SQL을 실행. 가장 느림.
reset_table()
# perf_counter(): 프로그램이 실행된 이후의 시간(초 단위)을
#                 정밀 측정해주는 함수
#              => 성능 측정용 시계
start = time.perf_counter()     # INSERT 하기 전 시각 체크

with conn.cursor() as cur:
    for r in rows:
        cur.execute(INSERT_SQL, r)
conn.commit()
t1 = time.perf_counter() - start
results.append(("1. execute 반복", t1, count_rows()))

# ---------------------------------------------------------
# 2. executemany -> 같은 SQL을 한 문장으로 한 번에 실행
reset_table()
start = time.perf_counter()

with conn.cursor() as cur:
    cur.executemany(INSERT_SQL, rows)
conn.commit()
t2 = time.perf_counter() - start
results.append(("2. executemany", t2, count_rows()))

# ----------------------------------------------------------
# # 3. to_sql -> 내부적으로 executemany를 사용하여 적재.
# """
#     df.to_sql(테이블명, engine, if_exists="append", index=False)

#     - if_exists
#         1) "append"  : 데이터 추가
#         2) "replace" : 테이블을 지우고 새로 만듦
#         3) "fail"    : 실패 처리
#     - INSERT문을 작성하지 않아도 알아서 실행해준다.
# """
# reset_table()
# start = time.perf_counter()

# sample.to_sql("daily_price", engine, if_exists="append", index=False)
# t3 = time.perf_counter() - start

# results.append(("3. to_sql", t3, count_rows()))

# # ------------------------------------------------------
# # 4. to_sql(method="multi") 
# # -> 원하는 개수만큼 쪼개서(청킹하여) 데이터를 적재
# reset_table()
# start = time.perf_counter()

# sample.to_sql("daily_price", engine, if_exists="append", index=False,
#               method="multi", chunksize=500)
# t4 = time.perf_counter() - start

# results.append(("4. to_sql(method='multi')", t4, count_rows()))

# ------------------------------------------------------
for name, t, n in results:
    print(f"{name:<20} {t*1_000:>8.0}ms {n:>8,}")

# 1. execute 반복           7e+01ms    1,000
# 2. executemany          1e+01ms    1,000

# 3, 4는 버전/툴 차이로 테이블 생성부터 다시 해야 해서 사용법만 남겨둠.
