"""
    설정 - 환경변수, 상수

    공통으로 사용되는 값을 정의하기 위한 용도
"""
import os

from _db import (connect, get_engine, ENCODING, KHLAB_BASE, 
                 data_path, prices_path, raw_prices_path)

# --------------------- 환경 변수 기반 설정 ---------------------
# Extract 방식: "api" 또는 "csv"
SOURCE = os.getenv("PIPELINE_SOURCE", "csv")

# API 페이지 상한
MAX_PAGES = int(os.getenv("PIPELINE_MAX_PAGES", 5))

# --------------------- 고정 상수 ---------------------
# 한 페이지에 요청할 데이터 수
PAGE_SIZE = 100

# DB에 적재 시에 사용할 청크 사이즈 (쪼개어 실행할 수)
CHUNK_SIZE = 5_000

# 서버 응답에 대한 타임아웃 시간 (초)
TIMEOUT = 5

# 요청 간의 대기 시간 (초) (적어도 1초씩은 대기)
DELAY = 1.0

# --------------------- 로그 경로 ---------------------
# 로그 기록 폴더 경로 및 폴더이름(logs) 설정
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
# => ../11_pipeline/logs
