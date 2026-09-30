"""
    멱등성과 UPSERT
"""
import time
import pandas as pd

from _db import connect, get_engine, prices_path, ENCODING

N = 2_000
conn = connect()
engine = get_engine()

df = pd.read_csv(prices_path(), encoding=ENCODING, parse_dates=["date"])
cols = ["code", "date", "open", "high", "low", "close", 
        "volume", "change", "changeRate"]

sample = df.head(N)[cols].copy()    # 2000개 데이터 복제

# rows 변수에 df -> list(tuple)로 변환하여 저장
rows = [tuple(c) for c in sample.itertuples(index=False)]

def quote(c):
    """컬럼명 c에 큰따옴표("")가 필요하면 "{c}", 아니면 c 그대로 반환"""
    return f'"{c}"' if c in ("date", "change", "changeRate") else c

# 컬럼명을 콤마로 구분하여 문자열로 엮어주기 (결과물은 아래처럼)
# code, "date", open, high, low, close, volume, "change", "changeRate"
COL_SQL = ", ".join(quote(c) for c in cols)
# 자리표시자 PlaceHolder 자동생성
PH = ", ".join([f":{i + 1}" for i in range(len(cols))])

def make_table(name, unique=False):
    """
        실습용 테이블 생성 함수
        - name: 테이블명
        - unique: UNIQUE(code, date) 설정 여부
    """
    def drop_table(cur, name):
        try:
            cur.execute(f"DROP TABLE {name}")
        except Exception as e:
            if "ORA-00942" not in str(e):
                # raise: 지금 발생한 예외를 그대로 다시 밖으로 던지는 것
                raise

    with conn.cursor() as cur:
        drop_table(cur, name)

       # unique 제약조건 있을 때만 추가되도록 삼항연산으로 추가
        uk = ', UNIQUE(code, "date")' if unique else ''
        cur.execute(f"""
            CREATE TABLE {name}(
                id      NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                code    VARCHAR2(20)   NOT NULL,
                "date"  DATE           NOT NULL,
                open    NUMBER(20),
                high    NUMBER(20),
                low     NUMBER(20),
                close   NUMBER(20),
                volume  NUMBER(20),
                "change"     NUMBER(20),
                "changeRate" NUMBER(6, 2)
                {uk}
            )
        """)

def count(name):
    """전달받은 테이블의 행 개수를 조회하여 반환"""
    with conn.cursor() as cur:
        cur.execute(f"SELECT COUNT(*) FROM {name}")
        return cur.fetchone()[0]

"""
    UPSERT (Update or Insert)
    : 데이터가 없으면 추가, 있으면 수정 (갱신)
      => MERGE INTO 구문

    데이터의 중복을 방지하기 위해, 추가하기 전에 SELECT로 값의 존재를
    확인할 수는 있으나, 조회(SELECT, 1번) 후 추가 또는 갱신(INSERT/UPDATE, 2번)
    하므로 SQL을 2배로 적어야 함.
    => 추가 및 갱신을 동시에 진행할 수 있도록 UPSERT를 사용(적용)함.
"""
PLAIN = f"INSERT INTO {{t}} ({COL_SQL}) VALUES ({PH})"
# {t}는 이후에 .format(t="테이블명") 적용 예정.
# .format() 함수 적용할 때도 {}가 필요하므로 {}를 두 번 씌움.

# .items(): 딕셔너리의 key-value 쌍을 짝 지어 줄 때 사용
# .enumerate(): 순서 번호(인덱스)와 값을 짝 지어 줄 때 사용
MERGE_USING_SQL = ", ".join(f":{i + 1} AS {quote(c)}" for i, c in enumerate(cols))
# destination의 dst, source의 src
# 전달할 데이터를 USING을 사용하여 전달
# 파이썬에서 executemany()로 넘긴 파라미터 값들(:1, :2 등)을
# 오라클이 임시 테이블 src로 포장하여 MERGE 구문 안으로 집어넣음.
UPSERT = f"""
    MERGE INTO {{t}} dst
    USING (SELECT {MERGE_USING_SQL} FROM dual) src
    ON (dst.code = src.code AND dst."date" = src."date")
    WHEN MATCHED THEN
    -- 코드와 날짜가 같은 항목이 있는 경우
    -- dst 테이블을 src 테이블 내용으로 갱신
        UPDATE SET dst.open = src.open, dst.high = src.high, dst.low = src.low,
                              dst.close = src.close, dst.volume = src.volume,
                              dst."change" = src."change",
                              dst."changeRate" = src."changeRate"
    WHEN NOT MATCHED THEN
    -- 코드와 날짜가 같은 항목이 없는 경우
    -- src 테이블의 내용대로 삽입
        INSERT ({COL_SQL})
        VALUES (src.code, src."date", src.open, src.high, src.low, src.close,
                src.volume, src."change", src."changeRate")
"""
# ==============================================================================
cases = []

# 1. 유니크 제약조건 없이 실행
make_table("t_noconstraint", unique=False)

for i in (1, 2):    # 2번 반복 실행
    with conn.cursor() as cur:
        # PLAIN의 {t} 위치에 t_noconstraint가 대입
        cur.executemany(PLAIN.format(t="t_noconstraint"), rows)
    conn.commit()

n1 = count("t_noconstraint")
print(f"[CASE 1] UNIQUE 제약조건 없이 실행: {n1} 행 추가")
# [CASE1] UNIQUE 제약조건 없이 실행: 4000 행 추가
cases.append(("[CASE 1] 제약조건 없이 INSERT 반복", "성공", n1, "데이터 두 배"))
print()

# 2. 유니크 제약조건 설정, INSERT 반복
make_table("t_unique", unique=True)

with conn.cursor() as cur:
    cur.executemany(PLAIN.format(t="t_unique"), rows)
conn.commit()

try:
    with conn.cursor() as cur:
        cur.executemany(PLAIN.format(t="t_unique"), rows)
    conn.commit()
    r2 = "성공"
except Exception as e:
    conn.rollback()
    r2 = type(e).__name__

n2 = count("t_unique")
cases.append(("[CASE 2] 제약조건 설정 후 INSERT 반복",
               r2, n2, "두 번째 실행 시 오류 발생"))
print()

# 3. 유니크 제약조건 설정 + UPSERT (MERGE INTO)
make_table("t_upsert", unique=True)

for i in (1, 2):
    with conn.cursor() as cur:
        cur.executemany(UPSERT.format(t="t_upsert"), rows)
    conn.commit()
n3 = count("t_upsert")
cases.append(("[CASE 3] 제약조건 설정 + UPSERT 반복", "성공",
               n3, "데이터 추가 후 재실행 시 갱신됨"))

print((f"{'방식':<36}{'결과':<10}{'행 수':>10}{'설명':>25}"))
for name, res, n, desc in cases:
    print(f"{name:<30}{res:<10}{n:>10}{desc:>25}")
"""
방식                                 결과           행 수                 설명
[CASE 1] 제약조건 없이 INSERT 반복    성공            4000             데이터 두 배
[CASE 2] 제약조건 설정 후 INSERT 반복  IntegrityError 2000     두 번째 실행 시 오류 발생
[CASE 3] 제약조건 설정 + UPSERT 반복  성공            2000  데이터 추가 후 재실행 시 갱신됨
"""

"""
    [CASE 1] 제약조건이 없을 경우, 오류도 없음.
    --> 중복된 데이터가 무한히 추가될 수 있음.
        추후 집계 시 이상한 결과를 도출할 수 있는데,
        되돌리고 싶어도 쉽지 않음.

    [CASE 2] 제약조건을 설정하는 경우, 중복은 막을 수 있으나 재실행 불가
    
    [CASE 3] UPSERT를 사용하면 위의 문제들을 해결할 수 있음.
    --> 데이터가 있으면 갱신, 없으면 새로 추가
"""
# =====================================================================
print("-" * 60)
"""
    신규/갱신 건수를 실행 전후 전체 행수 비교를 통해 기록
    # (실행 후 행 수) - (실행 전 행 수) = (신규 건수) >= 0
    # (전체 행 수) - (신규 건수) = (갱신 건수)
"""
def upsert_with_stats(table, data, chunk=1000):
    """청크마다 커밋하면서 신규/갱신 건수를 집계하는 함수"""
    start = time.perf_counter()
    before_count = count(table)

    # range 함수의 간격을 chunk로 지정하여 지정한 단위 주기로 반복
    for i in range(0, len(data), chunk):
        # data를 chunk 단위로 슬라이싱
        part = data[i:i+chunk]

        with conn.cursor() as cur:
            cur.executemany(UPSERT.format(t=table), part)
        conn.commit()
    
    after_count = count(table)

    inserted_cnt = after_count -before_count
    updated_cnt = len(data) - inserted_cnt

    # (추가 건수, 갱신 건수, 실행 시간) 반환
    return inserted_cnt, updated_cnt, time.perf_counter() - start

make_table("t_stats", unique=True)

i1, u1, t1 = upsert_with_stats("t_stats", rows)
print(f"\n[적재] t_stats (1회차)")
print(f" 입력    :   {len(rows)}행")
print(f" 신규    :   {i1}행")
print(f" 갱신    :   {u1}행")
print(f" 시간    :   {t1:.2f}초")
print()

i2, u2, t2 = upsert_with_stats("t_stats", rows)
print(f"\n[적재] t_stats (2회차)")
print(f" 입력    :   {len(rows)}행")
print(f" 신규    :   {i2}행")
print(f" 갱신    :   {u2}행")
print(f" 시간    :   {t2:.2f}초")
"""
    [적재] t_stats (1회차)
    입력    :   2000행
    신규    :   2000행
    갱신    :   0행
    시간    :   0.11초


    [적재] t_stats (2회차)
    입력    :   2000행
    신규    :   0행
    갱신    :   2000행
    시간    :   0.07초
"""
print()

"""
    기록(로그, 출력)을 남기는 것은 중요하다.
      - 재실행 시 전부 갱신으로 확인된다면 멱등하게 동작된 것이고,
      - 전부 신규로 확인된다면 중복 데이터가 쌓이고 있다는 신호이다.
    위 데이터 기준으로 2회차 실행 시
      - 신규 0
      - 갱신 데이터길이와 동일
    위와 같이 확인된 것은 정상적이다.
"""
print("-" * 60)

expected = sample
actual = pd.read_sql(f"SELECT {COL_SQL} FROM t_stats", engine)
# print(actual.head())

checks = [
    ("행 수", len(expected), len(actual)),
    ("종목 수", expected['code'].nunique(), actual["code"].nunique()),
    # 원본 데이터 2,000개와 DB에 들어갔다가 다시 읽어온 데이터 2,000개가
    # 틀린 부분 없이 잘 들어갔는지 확인하는 부분이므로,
    # 종가의 합계나 평균 등을 그룹화하지 않고 전체 평균으로 비교한다.
    ("종가 합계", expected['close'].sum(), actual['close'].sum() ),
    ("종가 평균", expected['close'].mean(), actual['close'].mean()),
    ("거래량 합계", expected['volume'].sum(), actual['volume'].sum()),
    # 날짜 타입으로 보려면 expected['date'].min().date()
    ("최소 날짜", expected['date'].min(), actual['date'].min()),
    ("최대 날짜", expected['date'].max(), actual['date'].max()),
]

all_ok = True
for name, exp, act in checks:
    ok = str(exp) == str(act)
    all_ok &= ok
    print(f"{name:<14}{str(exp):>20}{str(act):>20} {'일치' if ok else '불일치':>4}")

print(f"모든 항목 일치: {all_ok}")
"""
    행 수                           2000                2000   일치
    종목 수                             3                   3   일치
    종가 합계                     42961424            42961424   일치
    종가 평균                    21480.712           21480.712   일치
    거래량 합계                  2079066345          2079066345   일치
    최소 날짜          2023-09-25 00:00:00 2023-09-25 00:00:00   일치
    최대 날짜          2026-09-07 00:00:00 2026-09-07 00:00:00   일치
    모든 항목 일치: True
"""

# 테스트 테이블 삭제
def drop_table(cur, name):
    """전달된 테이블을 삭제하는 함수"""
    try:
        cur.execute(f"DROP TABLE {name}")
    except Exception as e:
        if  "ORA-00942" not in str(e):
            pass

for t in ["t_noconstraint", "t_unique", "t_upsert", "t_stats"]:
    with conn.cursor() as cur:
        drop_table(cur, t)

conn.close()