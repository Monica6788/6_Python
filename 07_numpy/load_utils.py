"""
    실습 데이터를 불러오는 기능을 담은 모듈
"""
import numpy as np
from pathlib import Path

# __file__ : 현재 파일 경로를 알려주는 속성 같은 것
# Path(__file__)로 현재 파일의 경로를 가져온 후, 
# with_name()으로 이름만 제시한 값("prices.csv")으로 변경
CSV_PATH = Path(__file__).with_name("prices.csv")
# print(CSV_PATH)     # 확인용
N_DAYS = 750          # 거래 일수

_COLUMNS = {
    "code": 0,
    "date": 1,
    "open": 2,
    "high": 3,
    "low": 4,
    "close": 5,
    "volume": 6,
    "change": 7,
    "changeRate": 8
}

# 한 번 읽은 열(데이터)을 저장하는 용도
_cache = {}

def _read(col, dtype):
    """
        csv에서 하나의 열만 읽어서 1차원 배열로 리턴하는 함수
    """
    key = (col, str(dtype))

    if key not in _cache:
        if not CSV_PATH.exists():   # 파일이 존재하지 않으면 예외 발생시키기
            raise FileNotFoundError(f"{CSV_PATH} 파일을 찾을 수 없습니다.")

        # 읽은 파일을 _cache의 key값으로 저장
        _cache[key] = np.loadtxt(
            # 읽어올 파일 경로
            CSV_PATH,
            # 읽어올 자료의 타입 지정, 함수의 매개변수로 받아올 dtype 이용      
            dtype=dtype,
            # csv 파일 안의 데이터가 어떤 구분자로 구분되는지 알려주기
            delimiter=",",
            # 필요한 열 하나만 읽도록 설정, 함수의 매개변수로 받아올 col 이용
            usecols=_COLUMNS[col],
            # 첫 줄(열 제목)을 생략
            skiprows=1,
            encoding="utf-8-sig"
        )

    return _cache[key].copy()   # 원본이 아닌 복사본을 반환

def load_close_flat():  # 1차원 배열은 평평하니까 flat
    """
        종가 데이터만 1차원 배열로 리턴하는 함수
    """
    return _read("close", "int64")

def load_one_stock(idx = 0):
    """
        한 종목의 종가만 1차원 배열로 리턴하는 함수
        종목 하나당 750줄, 그 다음 종목은 그 다음 줄부터 750줄, ...
    """
    close_arr = load_close_flat()
    start = idx * N_DAYS    # N_DAYS = 750
    end = start + N_DAYS
    return close_arr[start:end]        # 0 ~ 749

def load_dates():
    """
        거래일 정보를 날짜형식의 1차원 배열로 리턴하는 함수

        .astype("datetime64[D]") => 문자열을 날짜로 변경
        [D] => Day 단위로 다루겠다는 의미
    """
    dates = _read("date", str)
    return dates[:N_DAYS].astype("datetime64[D]")

def load_codes():
    """
        종목 코드 배열을 리턴하는 함수
    """
    codes = _read("code", str)
    # 750개씩 같은 코드가 반복되므로 N_DAYS(=750)을 사용하여 슬라이싱
    return codes[::N_DAYS]

def load_matrix():
    """
        종가 행렬을 반환하는 함수
        행: 종목 (120개) / 열: 날짜 (750개) --> (120, 750)
    """
    close = load_close_flat()           # 1차원 배열
    return close.reshape(120, 750)      # 2차원 배열

def load_column(name):
    """
        열 데이터를 행렬 (120, 750)로 반환하는 함수
    """
    if name in ("code", "date"):
        raise KeyError("기존 함수를 사용하세요.")

    if name not in _COLUMNS:
        raise KeyError("찾을 수 없는 열입니다.")

    # 문자열, 날짜 형식일 만한 컬럼은 읽어오는 함수를 따로 만들었음!
    # 나머지는 숫자 정보이므로 dtype을 실수/정수로 하여 읽어오도록 함수 정의
    dtype = "float64" if name == "changeRate" else "int64"

    return _read(name, dtype).reshape(120, 750)


