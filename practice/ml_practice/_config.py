"""
    공통 항목 설정
"""
import os

# ~/practice/ml_practice
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ~/practice/ml_practice/data
DATA_DIR = os.path.join(BASE_DIR, "data")
# ~/practice/ml_practice/models
MODELS_DIR = os.path.join(BASE_DIR, "models")

ENCODING = "utf-8-sig"

SEED = 42

def path(name):
    """data 폴더 안의 파일 경로 반환"""
    return os.path.join(DATA_DIR, name)

def rentals_path():
    """대여 기록(clean_rentals.csv) 파일 경로 반환"""
    local = path("clean_rentals.csv")
    return local

def users_path():
    """사용자(users.csv) 파일 경로 반환"""
    local = path("users.csv")
    return local