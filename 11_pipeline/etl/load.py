"""
    Load. 데이터를 DB에 적재 (저장)
    - 하지 않는 것: 정제(가공)
    - UPSERT를 사용하여 데이터가 있으면 UPDATE, 없으면 INSERT
    - 대용량을 한꺼번에 처리하지 않고,
      CHUNK_SIZE 단위로 나누어 처리
"""
import time

from .config import connect, CHUNK_SIZE

# DB에 저장할 컬럼 순서
COLS = ["code", "date", "open", "high", "low", "close", 
        "volume", "change", "changeRate"]

# 컬럼명에 큰따옴표 붙여야 하는 경우
def _quote(c):
    """
        컬럼명을 큰따옴표로 감싸서 반환
        Args.
            c: 컬럼명
    """
    return f'"{c}"' if c in ("date", "change", "changeRate") else c

# -------------------- SQL 조각 --------------------
# 컬럼 목록 문자열
# (컬럼명을 콤마로 구분하여 문자열로 엮어주기)
# code, "date", ... , volume, "change", ...
COL_SQL = ", ".join(_quote(c) for c in COLS)

# 위치 기반 바인드 변수 문자열
# (자리표시자 PlaceHolder 자동생성)
# :1, :2, ..., :8, :9
PH = ", ".join([f":{i + 1}" for i in range(len(COLS))])

# MERGE INTO 사용 시 별칭 지정
# :1 AS code, :2 AS "date", ...
MERGE_USING = ", ".join(f":{i + 1} AS {_quote(c)}"
                        for i, c in enumerate(COLS))


# 실행할 쿼리문
#   daily_price 테이블
UPSERT = f"""
MERGE INTO daily_price dst
USING (SELECT {MERGE_USING} FROM dual) src
ON (dst.code   = src.code AND
    dst."date" = src."date")
WHEN MATCHED THEN
    UPDATE SET dst.open         = src.open,
               dst.high         = src.high,
               dst.low          = src.low,
               dst.close        = src.close,
               dst.volume       = src.volume,
               dst."change"     = src."change",
               dst."changeRate" = src."changeRate"
WHEN NOT MATCHED THEN
    INSERT ({COL_SQL})
    VALUES (src.code, src."date", src.open, 
            src.high, src.low, src.close, src.volume, 
            src."change", src."changeRate")
"""

# -------------------- 함수 정의 --------------------
def _row_count(conn):
    """daily_price 테이블의 전체 행 수를 반환"""
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM daily_price")
        return cur.fetchone()[0]

def to_db(df, logger, chunk=CHUNK_SIZE):
    """
        UPSERT로 적재 후
        튜플 (신규 건수, 갱신 건수, 소요 시간)을 반환
    """
    # ----- 데이터 준비 -----
    # 필요한 열(COLS)만 선택
    # Pandas의 NaN -> Oracle이 이해할 수 있는 None(DBMS NULL) 변환
    # .astype(object): 모든 열을 파이썬 객체 타입으로 변환
    # where(df[COLS].notna(), None): NaN(float64임) -> None
    # oracledb가 Python None을 DBMS NULL로 처리
    data = df[COLS].astype(object).where(df[COLS].notna(), None)

    # list[tuple] 형태로 변환. 인덱스 없이 변환!
    # (executemany()에 집어넣기 위한 준비 과정)
    rows = [tuple(r) for r in data.itertuples(index=False)]

    # ----------------------
    conn = connect()

    # 타이머 시작
    start = time.perf_counter()

    # 적재 전 행 수 저장
    before = _row_count(conn)

    # 적재
    try:
        for i in range(0, len(rows), chunk):
            # 청크만큼 데이터 추출(슬라이싱)
            part = rows[i:i+chunk]

            with conn.cursor() as cur:
                # executemany(sql, param)
                cur.executemany(UPSERT, part)
            conn.commit()
    except Exception:
        conn.rollback()
        # 실패한 데이터의 인덱스 범위 -> WARNING 레벨 로그 기록
        logger.warning(f"   적재 실패 (범위: {i} ~ {i + chunk -1})")
        raise   # 상위 파이프라인에서 처리 예정
    finally:
        conn.close()

    # 적재 완료 후 새로운 커넥션 객체 생성
    # (행 수 변화의 정확한 측정을 위해 별도 생성)
    after_conn = connect()
    after = _row_count(after_conn)
    after_conn.close()

    # 신규 건수, 갱신 건수 계산
    #   (신규) = (적재 전 행 수) - (적재 후 행 수)
    #   (갱신) = (총 적재 시도 건수) - (신규)
    inserted = after - before
    updated = len(rows) - inserted
    time_interval = time.perf_counter() - start

    logger.info(f"  적재 완료\n"
                f"                      - 신규 {inserted}건\n"
                f"                      - 갱신 {updated}건\n"
                f"                      - 시간 {time_interval}")
    return inserted, updated, time_interval

def verify(df, logger):
    """
        적재 후 검증 결과 반환

        [검증 항목 - (df, db)]
        - 전체 행 수
        - 종목 코드 수
        - 종가 총합
        - 날짜 최소
        - 날짜 최대
    """
    conn = connect()

    with conn.cursor() as cur:
        cur.execute("""
            SELECT COUNT(*),
            -- 시세 데이터는 코드가 중복된 행이 많으니 DISTINCT로 중복 제거
                   COUNT(DISTINCT code),
                   SUM(close),
                   MIN("date"),
                   MAX("date")
            FROM daily_price
        """)
        # 전부 집계함수이므로 조회 결과는 1행 -> fetchone()
        row = cur.fetchone()
    conn.close()        # 명시적 close

    # 위의 쿼리문 실행 결과를 row라는 튜플로 관리 (DB결과)
    n, codes, close_sum, min_d, max_d = row

    def to_date_str(v):
        """전달된 datetime 데이터(value)의 날짜만 추출하여 문자열로 반환"""
        # hasattr(v, "date"): 전달받은 v가 "date"라는 속성을 갖는지 여부 반환
        # "date"라는 속성을 가지면 str(v.date()), 없으면 str(v)
        return str(v.date()) if hasattr(v, "date") else str(v)

    # {"검증항목명": (df기준_결과, db기준_결과), ...}
    checks = {
        "행 수": (len(df), n),
        "종목코드 수": (df["code"].nunique(), codes),
        # 파이썬에서는 type이 다르면 같은 값끼리도 False가 나올 수 있음
        # => close_sum은 int로 한 번 감싸서 타입을 맞추기.
        "종가 합계": (int(df["close"].sum()), int(close_sum)),
        # min_d, max_d가 초단위까지 나올 수 있음
        # => 시간 빼고 날짜만 나오도록 위에 정의한 함수 적용
        "최소 날짜": (str(df['date'].min().date()), to_date_str(min_d)),
        "최대 날짜": (str(df['date'].max().date()), to_date_str(max_d)),
    }

    all_ok = True
    # exp: expected, act: actual
    # checks는 딕셔너리, "name": (expected_value, actual_value) 형태
    for name, (exp, act) in checks.items():
        ok = str(exp) == str(act)
        all_ok &= ok

        logger.info(f"  {'OK' if ok else 'FAIL'} {name:<12} {exp} / {act}")
    
    return all_ok
