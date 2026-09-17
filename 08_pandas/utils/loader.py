"""
    실습용 데이터 로더 (데이터를 읽어오는 역할)
"""
import pandas as pd
from utils.config import RAW_PATH, ENCODING
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