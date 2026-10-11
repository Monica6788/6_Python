"""
    설정 - 환경변수, 상수

    공통으로 사용되는 값을 정의하기 위한 용도
"""
import os

from _db import connect, get_engine

# --------------------- 환경 변수 기반 설정 ---------------------
# Extract 방식: "csv"
SOURCE = os.getenv("PIPELINE_SOURCE", "csv")

# --------------------- 고정 상수 ---------------------
# DB에 적재 시에 사용할 청크 사이즈 (쪼개어 실행할 수)
CHUNK_SIZE = 5_000
ENCODING = "utf-8-sig"

# --------------------- 로그 경로 ---------------------
# 로그 기록 폴더 경로 및 폴더이름(logs) 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(os.path.dirname(
                        os.path.dirname(
                        os.path.abspath(__file__))),"data")

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
# => ../practice/public_bike/etl/logs

def data_path(name):
    """data 폴더 내의 파일 경로를 반환"""
    if not os.path.exists(DATA_DIR):
        raise FileNotFoundError("데이터셋이 없습니다.")
    return os.path.join(DATA_DIR, name)

def raw_bikes_path():
    """자전거 데이터 원본 파일 경로 반환"""
    # 파일 경로
    local_path = data_path("raw-bikes.csv")
    return local_path

def raw_rentals_path():
    """대여기록 데이터 원본 파일 경로 반환"""
    local_path = data_path("raw-rentals.csv")
    return local_path

def stations_path():
    """대여소 데이터 파일 경로 반환"""
    local_path = data_path("stations.csv")
    return local_path