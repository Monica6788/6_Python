"""
    데이터 점검
        - 각 파일의 행 수, 컬럼별 dtype
        - 숫자여야 하는데 문자열로 읽힌 컬럼
        - 컬럼별 결측 수와 비율
        - bike_id, rental_id 의 중복 건수
        - bike_type, district, payment_method의 고유값 목록
"""
import pandas as pd

from config import raw_bikes_path, raw_rentals_path, stations_path, ENCODING

raw_bikes = pd.read_csv(raw_bikes_path(), encoding=ENCODING,
                        dtype=str, keep_default_na=False)
raw_rentals = pd.read_csv(raw_rentals_path(), encoding=ENCODING,
                          dtype=str, keep_default_na=False)
stations = pd.read_csv(stations_path(), encoding=ENCODING)

# 각 파일의 행 수, 컬럼별 dtype
def row_count_dtype(df):
    return len(df)

# 숫자여야 하는데 문자열로 읽힌 컬럼

# 컬럼별 결측 수와 비율

# bike_id, rental_id 의 중복 건수


# bike_type, district, payment_method의 고유값 목록

