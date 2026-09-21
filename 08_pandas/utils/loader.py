"""
    실습용 데이터 로더 (데이터를 읽어오는 역할)
"""
import pandas as pd
from utils.config import RAW_PATH, ENCODING, path
# 현재 같은 패키지에 있어서 from .config도 가능하지만,
# 실행 환경에 따라 달라지지 않도록 패키지 경로까지 작성.

def load_csv(dedup=True):
    """
        실습용 csv 파일을 읽어와서 DataFrame을 반환하는 함수

        Args:
            dedup: 중복 제거 여부
    """
    df = pd.read_csv(RAW_PATH,
                encoding=ENCODING,
                na_values=["N/A", "-"],
                thousands=",")
    df['date'] = pd.to_datetime(df['date'], format='mixed')

    if dedup:
            # df.drop_duplicates: subset 설정 기준 중복 데이터 제거
            #   - subset: 중복을 제거할 기준 열
            #   - keep: 먼저 나온 데이터(first), 마지막 데이터(last), 모두 제거(False)
            df = df.drop_duplicates(subset=['code', 'date'], keep='first')

    # sort_values: 제시한 컬럼을 기준으로 정렬 -> 인덱스가 섞일 수 있음
    # reset_index(drop=True): 인덱스를 다시 0, 1, 2, ...로 지정해줌

    # 정렬한 후에 인덱스가 뒤죽박죽이 되지 않도록 reset_index()
    # 원래 인덱스를 버리기 위해 drop=True
    return df.sort_values(["code", "date"]).reset_index(drop=True)

def load_prices():
    """prices.csv 파일을 읽어서 df로 반환"""
    return pd.read_csv(path("prices.csv"), encoding=ENCODING, parse_dates=["date"])

def load_companies(raw=False):
    """
        raw=True일 때는 raw-companies.csv
        raw=False일 때는 companies.csv 파일을 읽어서 df로 반환
        
        companies.csv => 정제본. 결측 0.
        raw-companies.csv => 오염본 (공백, 대소문자, 중복, 전각 존재)
    """
    if raw:
        return pd.read_csv(path('raw-companies.csv'), encoding=ENCODING,
                    dtype=str, keep_default_na=False)
    else:
        return pd.read_csv(path('companies.csv'), encoding=ENCODING)


def load_sectors():
     """종목 섹터 데이터를 불러와서 DataFrame으로 반환"""
     return pd.read_csv(path("sectors.csv"), encoding=ENCODING)

def load_merged():
    """시세(prices), 종목(companies), 섹터(sectors) 데이터를 결합하여 df로 반환"""
    prices = load_prices()
    companies = load_companies()
    sectors = load_sectors().rename(columns={"code":"sectorCode", "name":"sector"})

    full = (prices.merge(companies[["code", "name", "sectorCode", "market"]],
                  on="code", how="left", validate="many_to_one")
                  # 오른쪽 키 값이 유일하도록 validate 지정
            .merge(sectors[["sectorCode", "sector"]],
                   on="sectorCode", how="left", validate="many_to_one")
    )   # 괄호로 통째로 묶어주면 .merge()를 이어서 진행 가능

    return (full.drop(columns=["sectorCode"])
                .sort_values(["code", "date"])
                .reset_index(drop=True))