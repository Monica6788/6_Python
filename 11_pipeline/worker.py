"""
    데이터 파이프라인, 재실행 검증
"""
from etl._db import connect
from etl.pipeline import run

# daily_price 테이블 초기화
conn = connect()

with conn.cursor() as cur:
    cur.execute("TRUNCATE TABLE daily_price")

def row_count():
    """daily_price 테이블 행 수 조회"""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM daily_price")
        return cur.fetchone()[0]

print("========== 1회차 실행 ==========")
print()

ok1 = run()
n1 = row_count()

print("========== 2회차 실행 ==========")
print()

ok2 = run()
n2 = row_count()

print("=" * 60)
print("========== 검증 ==========")
print("=" * 60)

# 재실행 검증
checks = [
    ("1회차 성공", ok1),
    ("2회차 성공", ok2),
    ("행 수 비교", n1 == n2),
    ("종목 수", None)
]

with conn.cursor() as cur:
    cur.execute("SELECT COUNT(DISTINCT code) FROM daily_price")
    codes = cur.fetchone()[0]
# 리스트(가변) 안의 원소를 새로운 튜플로 갈아치운 것
# 튜플 자체를 변경한 것이 아니므로 오류 X
checks[3] = ("종목 수", codes)

print(f"1회차 적재: {n1:,}행")
print(f"1회차 적재: {n2:,}행")
print(f"종목 수: {codes}")
print()

for name, ok, in checks:
    print(f"{name}: {'PASS' if ok else 'FAIL' }")

conn.close()

