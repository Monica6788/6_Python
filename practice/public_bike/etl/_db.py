"""
    DB 접속 관련 공통 모듈

    - 접속 정보는 .env에서만 읽을 것임 
      => 코드 상에 비밀번호를 저장하지 않음
"""
import os
import oracledb

# 환경변수 관련 처리
from dotenv import load_dotenv
from sqlalchemy import create_engine

# .env 파일을 읽어서 os.envrion에 저장 (채워줌)
load_dotenv()

# os.getenv('키값', 기본값): 환경변수에서 키값에 해당하는 값을 반환
#                           (기본값을 제시하는 경우 값이 없을 때 사용)
HOST = os.getenv("DB_HOST", '127.0.0.1')
PORT = int(os.getenv("DB_PORT", 1521))
NAME = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")

# 현재 실행 중인 파일의 폴더 기준, 그 안에 있는 data 폴더의 절대경로 저장
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
ENCODING = "utf-8-sig"

def connect(autocommit=False):
    """
        오라클에 연결 후 커넥션 객체를 반환하는 함수
        
        Args:
            autocommit: 자동 커밋 설정 (기본값 False)
    """
    # 오라클에 연결. DDL, UPSERT처럼 세밀한 작업 및 제어가 필요할 때 사용
    conn = oracledb.connect(
        user=USER,
        password=PASSWORD,
        dsn=f"{HOST}:{PORT}/{NAME}",    # localhost:1521/xe 형태
    )
    conn.autocommit = autocommit
    return conn

def get_engine():
    """SQLAlchemy 엔진을 반환하는 함수"""
    url = f"oracle+oracledb://{USER}:{PASSWORD}@{HOST}:{PORT}/?service_name={NAME}"
    return create_engine(url, pool_pre_ping=True)

def data_path(name):
    """data 폴더 내의 파일 경로를 반환"""
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