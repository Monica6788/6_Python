"""
    그룹화 기초 (groupby)
        - agg / tranform
"""
import pandas as pd
from utils.loader import load_csv

# 출력창 크기 설정
pd.set_option("display.width", 130)

# 데이터 불러오기
df = load_csv()

# agg: 그룹 당 한 줄 (한 행)

# 'code' 열을 기준으로 평균 조회
# SQL: SELECT code, AVG(close) FROM prices GROUP BY code (종목 기준 평균 조회)
# Pandas
mean_by_code = df.groupby('code')["close"].mean()
print(f"{'=' * 20} 종목 코드별 평균 {'=' * 20}")
print(f"{len(mean_by_code)} 행")
print(mean_by_code.head().round())
print()

# 여러 개를 한 번에 집계
print(f"{'=' * 20} 여러 통계를 한 번에 집계 {'=' * 20}")
summary = df.groupby('code').agg(
    평균종가=("close", "mean"),     # "close"컬럼에 대하여 mean() 함수 호출
    최고가=("close", "max"),        # "close" 컬럼에 대하여 max()함수 호출
    거래일수=("date", "count")      # "date" 컬럼에 대하여 count() 함수 호출
)
print(f"{len(summary)} 행")
print(summary.head())
print()

"""
    .agg(
        새로운_열_이름=("계산대상이될_기존컬럼명" "적용할_함수이름"),
        ...
    )
"""

# transform : 결과 행이 원본과 같은 길이로 반환
# 추가적인 작업이 필요한 경우 형태를 맞춰야 하므로 transform
# 단순히 확인만 하려면 agg
print(f"{len(df.groupby('code')['close'].transform('mean'))} 건")
print(df.tail())


"""
    # agg : 여러 집계를 한 번에 확인하고자 할 때 사용
        df.groupby(기준열).agg(새로운_열_이름=("대상_열_이름", "집계함수"), ...)
        => 그룹 수만큼 행 반환
        => 그룹화하여 어떤 결과를 요약해서 볼 수 있음
    
    # transform : 그룹별로 계산하되, 기존 df와 연산을 수행하기 위해
                  결과를 각 행의 원래 자리에 표시함.
        df.groupby("기준열")["대상열"].transform("집계함수")
        => 데이터 개수만큼 행 반환
        => 결과를 가지고 다음 연산을 수행할 수 있음.
"""
