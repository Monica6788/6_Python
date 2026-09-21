"""
    공통 변수 (설정 항목)
"""
from pathlib import Path

# Path(__file__)로 현재 파일 위치 잡고,
# 상위 폴더(utils 폴더)의 상위 폴더(08_pandas) 경로 잡아두기
BASE_DIR = Path(__file__).parent.parent
# data 폴더 위치 잡기
DATA_DIR = BASE_DIR

# raw-prices.csv 경로 잡기
CSV_PATH = DATA_DIR / "vgsales.csv"

ENCODING = "utf-8-sig"

def path(name):
    """
        data 폴더 안의 파일 경로를 반환
    """
    return DATA_DIR / name

