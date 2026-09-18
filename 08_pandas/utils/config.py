"""
    공통 변수 (설정 항목)
"""
from pathlib import Path

# Path(__file__)로 현재 파일 위치 잡고,
# 상위 폴더(utils 폴더)의 상위 폴더(08_pandas) 경로 잡아두기
BASE_DIR = Path(__file__).parent.parent
# data 폴더 위치 잡기
DATA_DIR = BASE_DIR / "data"

# raw-prices.csv 경로 잡기
RAW_PATH = DATA_DIR / "raw-prices.csv"

ENCODING = "utf-8-sig"

# 정제 단계별로 중간 결과물을 저장할 경로 추가
STEP_DIR = DATA_DIR / "steps"
# 폴더가 없으면 생성
STEP_DIR.mkdir(parents=True, exist_ok=True)

def step_path(filename):
    """단계별 저장된 파일 경로를 반환"""
    return STEP_DIR / filename


def path(name):
    """
        data 폴더 안의 파일 경로를 반환
    """
    return DATA_DIR / name

