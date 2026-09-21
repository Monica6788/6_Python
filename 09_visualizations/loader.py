"""
    데이터 로드
"""
import pandas as pd
from config import path, ENCODING

def load_prices(dedup=True):
    """
        prices.csv 파일을 읽어서 df 반환
        (날짜열을 날짜 타입으로 변환)
    """
    # df = pd.read_csv(path("prices.csv"), encoding=ENCODING,
    #                  parse_dates=['date'])
    # # if dedup:
    # #     df = df.drop_duplicates(subset=["code", "date"], keep="first")

    # return df.sort_values(["code", "date"]).reset_index(drop=True)
    return pd.read_csv(path("prices.csv"), encoding=ENCODING, parse_dates=["date"])

def load_companies():
    """companies.csv 파일을 읽어서 df 반환"""
    return pd.read_csv(path("companies.csv"), encoding=ENCODING)

def load_sectors():
    """sectors.csv 파일을 읽어서 df 반환"""
    return pd.read_csv(path("sectors.csv"), encoding=ENCODING)

