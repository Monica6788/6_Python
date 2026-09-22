"""
    연습문제 5 - 케글

    Video Game Sales
    vgsales.csv 파일을 읽어와서 아래 문제들을 해결해보시오.

    Ref.
    https://www.kaggle.com/code/upadorprofzs/eda-video-game-sales/
"""
import pandas as pd

from practice_05.loader import load_csv

"""
    문제 1. 데이터 구조 파악

    데이터의 행 수, 열 수를 출력하시오.
    결측치가 있는 컬럼을 찾아 개수를 함께 출력하시오.
"""
df = load_csv()
# df.info()
"""
    RangeIndex: 11917 entries, 0 to 11916
    Data columns (total 11 columns):
    #   Column        Non-Null Count  Dtype  
    ---  ------        --------------  -----  
    0   Rank          11917 non-null  int64  
    1   Name          11917 non-null  str    
    2   Platform      11917 non-null  str    
    3   Year          11716 non-null  float64   결측이
    4   Genre         11917 non-null  str    
    5   Publisher     11859 non-null  str       있을 법
    6   NA_Sales      11917 non-null  float64
    7   EU_Sales      11917 non-null  float64
    8   JP_Sales      11917 non-null  float64
    9   Other_Sales   11917 non-null  float64
    10  Global_Sales  11917 non-null  float64
    dtypes: float64(6), int64(1), str(4)
    memory usage: 1.0 MB
"""

# 데이터의 행, 열 수 출력
print(f"{df.shape[0]}행 {df.shape[1]}열")
print()

# 결측치가 있는 컬럼을 찾아 개수를 함께 출력
na = df.isna().sum()
for col in df.columns:
    if na[col] > 0:
        print(f"{col} 컬럼: {na[col]}개")
print()

# ---------------------------------------------------------
"""
    문제 2. 연도 (Year) 컬럼 정리

    Year 컬럼의 최솟값, 최댓값, 가장 많이 등장하는 연도를 각각 구하시오.
    출시 연도가 없는 데이터를 제거한 새로운 데이터 프레임을 만드시오.
"""
# Year 컬럼의 최솟값, 최댓값, 최빈값
print(f"Year 컬럼 최댓값: {df['Year'].max():.0f}")
print(f"Year 컬럼 최솟값: {df['Year'].min():.0f}")
mode = df["Year"].mode()[0]
count = df["Year"].value_counts()[mode]
print(f"Year 컬럼 최빈값: {mode:.0f} (횟수: {count:,}회)")
print()

# 출시 연도가 없는 데이터를 제거한 df
df_clean = df.dropna(subset=["Year"])

# ---------------------------------------------------------
"""
    문제 3. 주요 컬럼의 고유값 탐색

    Platform, Genre, Publisher 각각 어떤 값들이 있는 지 고유값 목록을 출력하시오.
    Genre는 총 몇 종류인지 구하시오.
"""
print(f"Platform 고유값 목록: {df['Platform'].unique()}\n")
print(f"Genre 고유값 목록: {df['Genre'].unique()}\n")
print(f"Genre 고유값 종류: {df['Genre'].nunique()}종\n")
print(f"Publisher 고유값 목록: {df['Publisher'].unique()}")
print()

# ---------------------------------------------------------
"""
    문제 4. 연도별 게임 출시 수

    연도별 게임 출시 개수를 구하고, 연도 오름차순으로 정렬하시오.
"""
games_by_years = df.set_index("Year").sort_index().groupby("Year")["Name"].count()
print(games_by_years)

# ---------------------------------------------------------
"""
    문제 5. 플랫폼별 전 세계 판매량

    플랫폼(Platform) 별로 Global_Sales를 합산하고, 
    판매량이 높은 순으로 TOP 10을 조회하시오.
"""
sales_by_platform = df.groupby("Platform")["Global_Sales"]

# ---------------------------------------------------------
"""
    문제 6. 가장 많이 판매된 장르

    장르별 Global_Sales 총합을 구해 가장 높은 장르를 찾으시오.
"""

# ---------------------------------------------------------
"""
    문제 7. Publisher 별 평균 판매량

    Publisher 별 평균 Global_Sales를 구하고, 상위 10개만 출력하시오.
"""

# ---------------------------------------------------------
"""
    문제 8. Publisher 별 가장 많이 발매한 장르

    각 Publisher가 가장 많이 만든 장르는 무엇인지 구하시오.
    (Publisher 별로 Genre count의 최대값 찾기)
    [hint] groupby(['Publisher', 'Genre']).size().reset_index()
"""

# ---------------------------------------------------------
"""
    문제 9. 국가별로 인기 있는 장르

    NA / EU / JP 각각 판매량이 가장 높은 장르를 구하시오.
"""
