"""
    Transform: 데이터 정제, 계산, 검증
"""
import numpy as np
import pandas as pd
import unicodedata

from .extract import raw_bikes,raw_rentals, stations, logger

BIKES_NUM_COLS = ["gear_count", "daily_fee", "manufacture_year"]
RENTALS_NUM_COLS = ["distance_km", "fee"]

def clean_bikes(records, logger=logger):
    """
        자전거 데이터 정제 및 정제 단계별 로그 기록
        - 포맷 통일: station_id 대문자로 통일, 빈 값은 결측 처리
                     bike_type 일반/전동 2종으로 통일
        - 타입 정제: gear_count 단위문자('단') 제거 및 정수로 변환
                     daily_fee 콤마 제거 후 정수로 변환
                     manufacture_year 정수로 변환, 변환 실패 시 결측 처리
        - 결측 (삭제 또는 보간): 요구사항 없음
        - 중복 제거: bike_id 기준
        - 이상치 처리: 요구사항 없음
    """
    # 1. DataFrame 변환
    bikes = pd.DataFrame(records)
    # 1-1. 로그 기록 (최초 입력 데이터 행 수)
    logger.info(f"  입력: {len(bikes):,}행")

    # 2. 포맷 통일
    #    station_id 대문자로 통일 및 빈 값을 결측 처리
    bikes["station_id"] = bikes["station_id"].replace("", np.nan)
    bikes["station_id"] = bikes["station_id"].str.upper()
    #    bike_type을 일반/전동 2종으로 통일
    #    진단 단계에서 확인한 bike_type 고유값 목록
    #    : ['일반　', '일 반', '일반', '전동', 'electric', '일반형']
    bikes["bike_type"] = (bikes["bike_type"]\
                                .apply(lambda s: unicodedata.normalize("NFKC", s)))
    bikes["bike_type"] = (bikes["bike_type"]
                                .replace(r"\s+", "").replace(r"형$", "", regex=True)
                                .replace("electric", "전동", regex=False))

    # 3. 숫자 타입 정제 (콤마 제거 + 변환 실패 시 NaN 처리)
    for col in BIKES_NUM_COLS:
        if col in bikes.columns:
            bikes[col] = pd.to_numeric(
                (bikes[col].astype(str)
                               .str.replace("단", "", regex=False)
                               .str.replace(",", "", regex=False)),
                errors="coerce")
    # 3-1. 로그 기록 (타입 정제 후 행 수)
    logger.info(f"  타입 정제 후 {len(bikes):,}행")

    # 4. bike_id 기준 중복 제거
    before = len(bikes)     # 로그 기록용 중복제거 전 행 수
    bikes = bikes.drop_duplicates(subset=["bike_id"], keep="first")

    # 4-1. 중복 제거 후 행 수, 제거된 건수
    row_count_diff = len(bikes) - before
    logger.info(f"중복 제거 후 {len(bikes):,}행 ({row_count_diff:,}건)")

    return bikes

# -------------------------------------------------------------------------
def clean_rentals(records, logger=logger):
    """
        대여기록 데이터 정제 및 정제 단계별 로그 기록
        - 타입 정제: distance_km, fee 콤마 제거 후 숫자로 변환, 실패 시 결측 처리
                     rent_time, return_time: datetime으로 통일 (형식 3종 혼재)
        - 포맷 통일: payment_method 공백 제거 후 대문자로 통일
        - 중복 제거: rental_id 기준 중복 제거
    """
    # 1. DataFrame 변환
    rentals = pd.DataFrame(records)
    # 1-1. 로그 기록 (최초 입력 데이터 행 수)
    logger.info(f"  입력: {len(rentals):,}행")

    # 2. 숫자 타입 정제
    for col in RENTALS_NUM_COLS:
        if col in rentals.columns:
            rentals[col] = pd.to_numeric(
                    rentals[col].astype(str)
                                .str.replace(",", "", regex=False),
                    errors="coerce")

    # 3. 날짜 타입 정제
    for col in ["rent_time", "return_time"]:
        if col in rentals.columns:
            rentals[col] = pd.to_datetime(
                rentals[col], format="mixed", errors="coerce"
            )

    # 4. 포맷 통일
    rentals["payment_method"] = (rentals["payment_method"]
                                        .apply(lambda s: unicodedata.normalize("NFKC", s)))
    rentals["payment_method"] = (rentals["payment_method"].astype(str)
                                        .str.replace(r"\s+", "", regex=True).str.upper())

    # 4-1. 로그 기록 (타입 정제 후 데이터 행 수)
    logger.info(f"  타입 정제 후 {len(rentals):,}행")

    # 5. 중복 제거
    before = len(rentals)
    rentals = rentals.drop_duplicates(subset=["rental_id"], keep="first")

    # 5-1. 로그 기록 (중복 제거 후 행 수 및 제거된 건수)
    row_count_diff = before - len(rentals)
    logger.info(f"  중복 제거 후 {len(rentals):,}행 ({row_count_diff:,}건)")

    return rentals

#--------------------------------------------------------------------------------------------
# STEP 4. 데이터 결합
bikes, _ = clean_bikes(raw_bikes())[0]
rentals, _ = clean_rentals(raw_rentals())[0]
df_stations = stations()[0]

# rental_log(merged_df) - rentals, bikes 합치기
rental_log = rentals.merge(
            bikes, how="left", on="bike_id", 
            validate="many_to_one", indicator=True
            )
# indicator=True: 매칭 성패 여부를 조사하여 "_merge"라는 컬럼을 만들어줌.
# "both": 양쪽 df에 다 있어서 매칭 성공
# "left_only": 왼쪽(여기서는 rentals)에만 있어서 매칭 실패

# merge 실패한 bikes는 rental_log에서 제외하기
bikes_failed = rental_log[rental_log["_merge"] != "both"]
logger.info(f"  확인 문항 1. 매칭에 실패한 bike_id와 그 건수")
logger.info(f"  {bikes_failed['bike_id'].tolist()}")
logger.info(f"  매칭 실패 (bike_id) {len(bikes_failed):,}건")
logger.info(f"  확인 문항 2. 이런 데이터를 실무에서 뭐라고 부릅니까? 어떻게 처리해야 합니까?")
logger.info(f"  고아 레코드(Orphan Record) 또는 참조 무결성 오류.")
logger.info(f"  부모 데이터에 해당 부모 데이터 추가 혹은 분석에서 제외.")
rental_log = rental_log[rental_log["_merge"] == "both"].drop(columns=["_merge"])

# rental_log - 위의 rental_log에 stations 합치기
rental_log = rental_log.merge(
                df_stations, how="left", on="station_id",
                validate="many_to_one", indicator=True
            )

# 매칭 안 된 stations 제외시키기
stations_failed = rental_log[rental_log["_merge"] != "both"]
logger.info(f"  매칭 실패 (station_id) {len(stations_failed):,}건")
rental_log = rental_log[rental_log["_merge"] == "both"].drop(columns=["_merge"])
logger.info(f"  확인 문항 3. 자치구명이 결측인 행이 있습니다. 원인은 무엇입니까?")
logger.info(f"  station_id를 이용하여 merge하는데,"
            f"  bikes에 station_id가 누락된 데이터가 존재하기 때문.")

# -----------------------------------------------------------------------------
# STEP 5. 이상치와 논리 검사
df = rental_log.copy()

def drop_outliers(df:pd.DataFrame):
    df["duration_min"] = df["return_time"] - df["rent_time"]

    # 데이터가 초 단위로 되어 있으므로 대여시각 = 반납시각이 같은 것도 X
    time_check = df["rent_time"] >= df["return_time"]
    logger.info(f"  대여/반납 시각 이상치: {len(df[time_check]):,}건")
    fee_check = df["fee"] < 0
    logger.info(f"  요금 이상치: {len(df[fee_check]):,}건")
    # duration_min이 분 단위인데 조건으로 제시된 속력이 시속, 즉 시간단위
    # => 60으로 나누어 시간단위로 변환
    # 반납시각이 대여시각보다 앞선 경우 time_check에서 걸리므로 계산 안 함
    speed_check =  ((df["duration_min"] > 0) &
                    (df["distance_km"] / (df["duration_min"] / 60) > 50)
                   )
    logger.info(f"  이동거리(속도) 이상치: {len(df[speed_check]):,}건")

    not_outliers = ~(time_check | fee_check | speed_check)
    clean_df = df[not_outliers].reset_index(drop=True), time_check, fee_check, speed_check
    logger.info(f"  이상치 제거 후 {len(clean_df):,}행")

    return clean_df

# -------------------------------------------------------------------------------
# STEP 6. 결측 처리
def handle_na(df: pd.DataFrame):
    df, tc, fc, sc = drop_outliers(df)

    # fee 결측 복원
    fee_na = df["fee"].isna().sum()
    logger.info(f"  fee 결측 {fee_na:,}건")
    df["fee_per_m"] = df["daily_fee"] / (24 * 60)
    df["duration_min"] = df["return_time"] - df["rent_time"]
    df["fee"] = df["fee"].fillna(df["fee_per_m"] * df["duration_min"])

    # distance_km 결측 버리기
    distance_na = df["distance_km"].isna().sum()
    logger.info(f"  distance_km 결측 {distance_na:,}건")
    df = df.dropna(subset=["distance_km"]).reset_index(drop=True)

    return df

# -------------------------------------------------------------------------
# STEP 7. 집계
df = handle_na(df)

def analysis():
    checks = {
        "행 수": f"{len(df)}행",
        "자전거 수": f"{df['bike_id'].nunique():,}대",
        "이용자 수": f"{df['user_id'].nunique():,}명",
        "총 이동거리": f"{df['distance_km'].sum():,.2f}km",
        "총 매출": f"{df['fee'].sum():,.0f}원",
        "평균 대여시간": f"{df['duration_min'].mean():,.1f}분",
        "\n자치구별 집계 (매출 내림차순)": f"{df.groupby('district').agg(
            건수=('rental_id', 'nunique'),
            이동거리=('distance_km', 'sum'),
            매출=('fee', 'sum')
        ).sort_values('매출', ascending=False)}",
        "\n자전거 타입별 집계": f"{df.groupby('bike_type').agg(
            건수=('rental_id', 'nunique'),
            평균이동거리=('distance_km', 'mean'),
            평균대여시간=('duration_min', 'mean')
        ).round(2)}"
    }
    for name, value in checks.items():
        print(f"{name}: {value}")

# 검증
def validate_bikes(df, logger):
    """
        bikes 검증
    """
    pass