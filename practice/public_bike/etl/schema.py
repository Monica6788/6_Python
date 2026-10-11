"""
    수집 데이터용 스키마 설계
"""
import pandas as pd
from _db import connect, ENCODING

conn = connect()

def drop_table(cur, name):
    try:
        cur.execute(f"DROP TABLE {name}")
    except Exception as e:
        if "ORA-00942" not in str(e):
            pass

# ------------ 원본 테이블 저장용 테이블 생성
# 자전거 데이터 원본 테이블
RAW_BIKES_DDL = """
CREATE TABLE raw_bikes (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bike_id VARCHAR2(20),
    station_id VARCHAR2(20),
    bike_type VARCHAR2(20),
    gear_count VARCHAR2(20),
    manufacture_year VARCHAR2(20),
    daily_fee VARCHAR2(20)
)
"""

# 대여기록 데이터 원본 테이블
RAW_RENTALS_DDL = """
CREATE TABLE raw_rentals (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rental_id VARCHAR2(20),
    bike_id VARCHAR2(20),
    user_id VARCHAR2(20),
    rent_time VARCHAR2(50),
    return_time VARCHAR2(50),
    distance_km VARCHAR2(20),
    fee VARCHAR2(20),
    payment_method VARCHAR2(30)
)
"""

# ------------ 정제 완료된 데이터 저장용 테이블
# 자전거 데이터 테이블
BIKES_DDL = """
CREATE TABLE bikes (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    bike_id VARCHAR2(20) NOT NULL,
    station_id VARCHAR2(20),
    bike_type VARCHAR2(10),
    gear_count NUMBER(1),
    manufacture_year NUMBER,
    daily_fee NUMBER
)
"""

# 대여기록 데이터 테이블
RENTALS_DDL = """
CREATE TABLE rentals (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    rental_id VARCHAR2(20) NOT NULL,
    bike_id VARCHAR2(20),
    user_id VARCHAR2(20),
    rent_time DATE,
    return_time DATE,
    distance_km NUMBER,
    fee NUMBER,
    payment_method VARCHAR2(30)
)
"""

# 대여소 데이터 테이블
STATIONS_DDL = """
CREATE TABLE stations (
    id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    station_id VARCHAR2(10) NOT NULL,
    station_name VARCHAR2(50),
    district VARCHAR2(15)
)
"""

# 대여 기록(bikes, stations 병합본) 테이블 DDL
RENTAL_LOG_DDL = """
CREATE TABLE rental_log (

)
"""