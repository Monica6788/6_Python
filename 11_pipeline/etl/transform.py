"""
    Transform : 데이터 정제, 계산, 검증

    - 하지 않을 것 : 저장(적재)

    Extract 단계에서 전달된 원본 데이터를 
            DB에 저장 가능한 상태로 만듦
    - 타입 변환 (문자열 -> 숫자/날짜)
    - 중복 제거
    - 이상치 탐지 / 결측치 처리 (제거/대치/보간)
    - 파생 컬럼(등락, 등락률 등) 계산 (재계산)
    - 검증
"""
import pandas as pd

from .extract import from_api, from_csv

# 수치형(숫자)으로 변환한 열 목록
NUM_COLS = ["open", "high", "low","close", 
            "volume", "change", "changeRate"]

# 보간 대상 목록 (OHLC - 시가, 고가, 저가 종가)
OHLC = ["open", "high", "low", "close"]

def clean_prices(records, logger):
    """
        정제 함수. 단계마다 건수를 로그로 기록.

        [처리 순서]
        1. list[dict] -> DataFrame 변환
        2. 숫자 타입 정제
        3. 날짜 타입 정제
        4. 종목 코드 정규화 (대문자, 공백 제거, ...)
        5. 중복 제거 (code, date 기준)
        6. 이상치 탐지 -> NaN 처리
        7. 결측 보간 (interpolate -> ffill -> bfill)
        8. OHLC 정합성
        9. 소수점 -> 정수 (반올림)
        10. 등락, 등락률 재계산
    """
    # 1. DataFrame 변환
    df = pd.DataFrame(records)
    # 1-1. 로그 기록 (최초 입력 데이터 행 수)
    logger.info(f"  입력 {len(df):,}행")

    # 2. 숫자 타입 정제 
    #    콤마 제거: 1,000 -> 1000
    #    변환 실패 시 NaN 처리
    for col in NUM_COLS:
        # df 안에 존재하는 컬럼일 때만 실행하도록 if문
        # (KeyError 방지)
        if col in df.columns:
            df[col] = pd.to_numeric(
                        # astype(str)
                        # 안전한 실행을 위해 시리즈 전체의
                        # 데이터 타입을 문자열로 변환하고,
                        # 접두사 .str과 함께 문자열 함수
                        (df[col].astype(str)
                                .str.replace(",", "", regex=False)),
                        errors="coerce"
                    )


    # 3. 날짜 타입 정제
    #    날짜 형식이 다르더라도 변환될 수 있도록 설정 => format="mixed"
    #    변환 실패 시 NaN 처리 => errors="coerce"
    df["date"] = pd.to_datetime(df["date"], format="mixed",
                                errors="coerce")

    # 4. 종목 코드 정규화
    #    "G0001" / " G0001" / "G0001 " / "g0001" / ...
    #    -> 대문자로 변경 + 공백 제거
    # astype(str): 혹시 모를 숫자/혼합 타입을 문자열로 통일
    df["code"] = df["code"].astype(str).str.upper().str.strip()

    # 4-1. 로그 기록 (타입 정제 후 데이터 행 수)
    logger.info(f"  타입 정제 {len(df):,}행")

    # 5. 중복 제거
    #    타입 정제 후 중복 데이터의 존재를 확인해야 함.
    before = len(df)    # 중복 제거 전 전체 행 수
    # 중복 제거 후 df 갱신
    df = df.drop_duplicates(subset=["code", "date"], keep="first")

    # 5-1. 로그 기록 (중복 제거 후 행 수, 줄어든 건수)
    #   {len(df) - before:+,} : +로 부호 표시, ,로 콤마 표시
    logger.info(f"  중복 제거 {len(df):,}행 ({len(df) - before:+,})")

    # 6. 이상치 탐지
    # 종목별 날짜순으로 정렬 후 인덱스 재정렬
    df = df.sort_values(["code", "date"]).reset_index(drop=True)

    def is_outlier(s):
        """
            s: 한 종목의 종가 Series

            [IQR 방식]
                Q1 (25분위수)와 Q3 (75분위수)를 구하고,
                IQR = Q3 - Q1으로 정의

                폐구간 [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR] 범위를
                벗어날 경우 이상치로 판단
        """
        q1, q3 = s.quantile([0.25, 0.75])
        iqr = q3 - q1

        return ((s < q1 - 1.5 * iqr) | (s > q3 + 1.5 * iqr))

    # 통계적 이상치
    stat = df.groupby("code")["close"].transform(is_outlier)

    # 논리적 이상치
    logic = ((df["close"] < df['low']) | (df['close'] > df['high']))

    # 통계적/논리적 이상치에 해당하는 건수
    # 불리언 인덱싱 활용
    n_out = int((stat | logic).sum())

    # 이상치로 판단된 종가 데이터를 판다스 결측치 개체인 NaN으로 변경
    df.loc[stat | logic, "close"] = pd.NA
    # 여기까지 진행된 후에는 float64 타입이 아니게 될 수 있음
    # (pd.NA가 들어가면 df의 컬럼 타입이 object 등으로 꼬일 수 있음!)
    # => 다시 float 형태의 NaN으로 형 변환 
    #    pd.NA -> float NaN(명시적 변환)
    df["close"] = pd.to_numeric(df["close"], errors="coerce")

    # 거래량(volume)이 음수인 경우 NaN으로 변경
    df.loc[df["volume"] < 0, "volume"] = pd.NA
    df["volume"] = pd.to_numeric(df["volume"], errors="coerce")

    # 6-1. 로그 기록 (이상치로 처리된 행 수)
    logger.info(f"  이상치 탐지/처리 {len(df):,}행"
                f" ({n_out:,}건 -> NaN)")

    # 7. 결측 보간
    #    interpolate() : 선형 보간.
    #                 => 앞뒤 값의 중간값으로 채우기
    #    ffill(): 직전 값으로 채우기 (forward fill)
    #    bfill(): 직후 값으로 채우기 (backward fill)
    for col in OHLC:
        df[col] = df.groupby("code")[col].transform(
            # lambda s: 한 종목의 특정 컬럼 Series를 받아서
            #           interpolate -> ffill -> bfill 순서대로 연산
            lambda s: s.interpolate().ffill().bfill()
        )

    # 8. OHLC 정합성 - clip 
    #   (주가 데이터의 논리적 무결성 보장)
    # 8-1. 정합성 처리 전 로그 기록
    logger.info(f"  OHLC 정합성 처리 전"
                f" (종가 결측: {df['close'].isna().sum():,}건)")
    
    # clip(lower=..., upper=...): 값의 범위를 자르는 메서드
    # => lower 미만은 lower값으로, upper 초과는 upper값으로 변경
    df["close"] = df["close"].clip(lower=df["low"], upper=df["high"])

    # 8-2. 정합성 처리 후 로그 기록
    logger.info(f"  OHLC 정합성 처리 후"
                f" (종가 결측: {df['close'].isna().sum():,}건)")
    
    # 9. 반올림
    #    OHLC => 실수 타입으로 처리 (결측, 보간, ...)
    #    DB(Oracle)에 해당 컬럼들이 NUMBER(20) 정수 형태임
    #    -> 반올림 처리로 DB 적재를 위한 타입을 맞춰주기
    # (소수점이 있는 상태로 적재 시 에러 발생 또는 데이터가 잘릴 가능성이 있음.)

    # 정수 형태가 아닌 값들 카운트 (로그 기록용)
    # 열별 합산을 위해 일단 .sum() 1회
    # 열별 합계값들의 합산을 위해 .sum() 1회 추가 (전체 함계)
    n_round = (df[OHLC] % 1 != 0).sum().sum()

    # OHLC 열 반올림 처리
    for col in OHLC:
        # 기본값이 0이긴 한데 그냥 명시해줌.
        df[col] = df[col].round(0)
    # 9-1. 로그 기록 (반올림 처리 후 행 수, 처리 대상 수)
    logger.info(f"  정수 반올림 처리 {len(df):,}행 (처리 대상: {n_round}개)")

    # 10. 등락, 등락률 재계산
    #    (비즈니스 로직 정합성 확보)
    # 종가 보간, 반올림 처리를 하면서 종가 데이터가 변경되므로,
    # 원본의 change, changeRate를 그대로 사용할 수 없음.
    # (수학적 정합성 유지를 위해 재계산 필수)

    # 종목별 직전(전일) 종가 prev 저장
    # shift(1): 종목별로 묶인 상태에서 행을 아래로 1칸씩 밀기
    #        => 오늘 행에 '어제(직전)의 종가' 하나가 위치하게 됨
    prev = df.groupby("code")["close"].shift(1)

    # 등락폭 재계산
    df["change"] = (df["close"] - prev).round()

    # 등락률 재계산
    df["changeRate"] = ((df["close"] - prev) * 100 / prev).round(2)

    # [FINAL] 정제가 완료된 최종 DataFrame 반환
    return df

def validate(df, logger):
    """
        정제 작업 완료 후 검증 결과를 확인하는 함수
        검증 실패 시 파이프라인 멈추기
        
        [검증 항목]
        - 날짜 타입 열이 datetime 타입인지
        - 중복 데이터가 없는지 (code, date 기준)
        - 종가 데이터에 결측이 없는지
        - OHLC 논리 정합성: 저가 <= 시가, 종가 <= 고가
        - 거래량이 음수가 아닌지
    """
    checks = [
        # [(항목이름, 검증결과), ...] 꼴
        ("날짜 타입 (datetime)", 
            pd.api.types.is_datetime64_any_dtype(df["date"])),
        ("중복 데이터 = 0 검증 (code, date)",
            df.duplicated(subset=["code", "date"]).sum() == 0),
        ("종가 데이터 결측 = 0 검증",
            df["close"].isna().sum() == 0),
        ("OHLC 정합성",
            bool(((df["low"] <= df["close"]) & 
                  (df["close"] <= df["high"])).all())),
        ("거래량이 음수인 데이터 = 0 검증",
            bool( (df["volume"].dropna() >= 0).all() ) ),
    ]

    # 실패한 항목의 이름(첫 번째)만 리스트로 저장
    # checks 리스트의 튜플 구조(name, ok)를 언패킹
    # => ok=False인 항목의 name만 수집
    failed = [name for name, ok in checks if not ok]

    # 로그 기록
    for name, ok in checks:
        logger.info(f"  {'[OK]' if ok else '[FAIL]'} {name}")

    if failed:
        raise ValueError(f"검증 실패: {failed}")

    # failed가 빈 list, 즉 실패한 항목이 없으면 True 반환
    return True