"""
    설정 - 환경변수, 상수

    공통으로 사용되는 값을 정의하기 위한 용도
"""
import os

from ._db import (connect, get_engine, ENCODING, KHLAB_BASE, 
                 data_path)

# --------------------- 환경 변수 기반 설정 ---------------------
# Extract 방식: "csv"
SOURCE = os.getenv("PIPELINE_SOURCE", "csv")

# --------------------- 고정 상수 ---------------------
# DB에 적재 시에 사용할 청크 사이즈 (쪼개어 실행할 수)
CHUNK_SIZE = 5_000

# --------------------- 로그 경로 ---------------------
# 로그 기록 폴더 경로 및 폴더이름(logs) 설정
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
# => ../practice/public_bike/etl/logs
