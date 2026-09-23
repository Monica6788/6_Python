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
print(f"{'=' * 24} 데이터의 행, 열 수 출력 {'=' * 24}")
print(f"{df.shape[0]}행 {df.shape[1]}열")
"""
    11917행 11열
"""
print()

# 결측치가 있는 컬럼을 찾아 개수를 함께 출력
print(f"{'=' * 24} 결측치를 가진 컬럼과 그 개수 {'=' * 24}")
na = df.isna().sum()
for col in df.columns:
    if na[col] > 0:
        print(f"{col} 컬럼: {na[col]}개")
"""
    Year 컬럼: 201개
    Publisher 컬럼: 58개
"""
print()

# ---------------------------------------------------------
"""
    문제 2. 연도 (Year) 컬럼 정리

    Year 컬럼의 최솟값, 최댓값, 가장 많이 등장하는 연도를 각각 구하시오.
    출시 연도가 없는 데이터를 제거한 새로운 데이터 프레임을 만드시오.
"""
# Year 컬럼의 최솟값, 최댓값, 최빈값
print(f"{'=' * 20} Year 컬럼의 최솟값, 최댓값, 최빈값 {'=' * 20}")
print(f"Year 컬럼 최댓값: {df['Year'].max():.0f}")
print(f"Year 컬럼 최솟값: {df['Year'].min():.0f}")
mode = df["Year"].mode()[0]
count = df["Year"].value_counts()[mode]
print(f"Year 컬럼 최빈값: {mode:.0f} (횟수: {count:,}회)")
"""
    Year 컬럼 최댓값: 2020
    Year 컬럼 최솟값: 1980
    Year 컬럼 최빈값: 2008 (횟수: 1,010회)
"""
print()

# 출시 연도가 없는 데이터를 제거한 df
print(f"{'=' * 20} 출시 연도가 없는 데이터를 제거한 df {'=' * 20}")
df_clean = df.dropna(subset=["Year"])
print(df_clean.info())
"""
    <class 'pandas.DataFrame'>
    Index: 11716 entries, 0 to 11916
    Data columns (total 11 columns):
    #   Column        Non-Null Count  Dtype  
    ---  ------        --------------  -----  
    0   Rank          11716 non-null  int64  
    1   Name          11716 non-null  str    
    2   Platform      11716 non-null  str    
    3   Year          11716 non-null  float64
    4   Genre         11716 non-null  str    
    5   Publisher     11680 non-null  str    
    6   NA_Sales      11716 non-null  float64
    7   EU_Sales      11716 non-null  float64
    8   JP_Sales      11716 non-null  float64
    9   Other_Sales   11716 non-null  float64
    10  Global_Sales  11716 non-null  float64
    dtypes: float64(6), int64(1), str(4)
    memory usage: 1.1 MB
    None
"""
print()

# ---------------------------------------------------------
"""
    문제 3. 주요 컬럼의 고유값 탐색

    Platform, Genre, Publisher 각각 어떤 값들이 있는 지 고유값 목록을 출력하시오.
    Genre는 총 몇 종류인지 구하시오.
"""
print(f"{'=' * 20} 플랫폼, 장르, 제작사별 고유값 목록 {'=' * 20}")
print(f"Platform 고유값 목록: {df['Platform'].unique()}\n")
print(f"Genre 고유값 목록: {df['Genre'].unique()}")
print(f"Genre 고유값 종류: {df['Genre'].nunique()}종\n")
print(f"Publisher 고유값 목록: {df['Publisher'].unique()}")
"""
    Platform 고유값 목록: <StringArray>
    [  'PS',  'PS2',  'PSP',  'PS3', 'X360',  'N64',   'DS',  'Wii',  '3DS',
    'PC',  'NES',  'GBA',   'XB',  'PSV',   'GC',  'PS4', 'SNES', '2600',
    'SAT',   'GB', 'WiiU',   'NG',  'GEN', 'PCFX',   'DC',  '3DO', 'XOne',
    'WS', 'TG16',  'SCD',   'GG']
    Length: 31, dtype: str

    Genre 고유값 목록: <StringArray>
    [      'Sports', 'Role-Playing',       'Action',       'Racing',
        'Shooter',         'Misc',    'Adventure',       'Puzzle',
    'Simulation',     'Platform',     'Strategy',     'Fighting']
    Length: 12, dtype: str
    Genre 고유값 종류: 12종

    Publisher 고유값 목록: <StringArray>
    [       'Magical Company',     'Namco Bandai Games',                  'Atari',
            'Electronic Arts',             'Activision',              'DSI Games',
                'Kaga Create',                'Ubisoft',               'Nintendo',
                'Rondomedia',
    ...
            'Team17 Software',               'Sold Out',               'Tryfirst',
            'Universal Gamex',   'Yamasa Entertainment',                   'Aria',
            'responDESIGN',    'Karin Entertainment', 'Rebellion Developments',
                'MediaQuest']
    Length: 579, dtype: str
"""
print()

# ---------------------------------------------------------
"""
    문제 4. 연도별 게임 출시 수

    연도별 게임 출시 개수를 구하고, 연도 오름차순으로 정렬하시오.
"""
print(f"{'=' * 24} 연도별 게임 출시 수 {'=' * 24}")
games_by_years = df.set_index("Year").sort_index().groupby("Year")["Name"].count()
print(games_by_years)
"""
    Year
    1980.0       9
    1981.0      46
    1982.0      36
    1983.0      16
    1984.0      14
    1985.0      14
    1986.0      21
    1987.0      16
    1988.0      13
    1989.0      14
    1990.0      14
    1991.0      40
    1992.0      40
    1993.0      60
    1994.0     116
    1995.0     205
    1996.0     254
    1997.0     278
    1998.0     354
    1999.0     301
    2000.0     307
    2001.0     420
    2002.0     598
    2003.0     518
    2004.0     547
    2005.0     648
    2006.0     740
    2007.0     864
    2008.0    1010
    2009.0     981
    2010.0     891
    2011.0     761
    2012.0     426
    2013.0     311
    2014.0     292
    2015.0     341
    2016.0     197
    2017.0       2
    2020.0       1
    Name: Name, dtype: int64
"""
print()

# ---------------------------------------------------------
"""
    문제 5. 플랫폼별 전 세계 판매량

    플랫폼(Platform) 별로 Global_Sales를 합산하고, 
    판매량이 높은 순으로 TOP 10을 조회하시오.
"""
print(f"{'=' * 20} 플랫폼별 전 세계 판매량 TOP 10 {'=' * 20}")
sales_by_platform = (df.groupby("Platform")["Global_Sales"]
                       .sum().sort_values(ascending=False))
print(sales_by_platform.head(10))
"""
    Platform
    PS2     1141.72
    Wii      804.17
    DS       714.91
    PS       705.90
    X360     581.86
    PS3      561.08
    GBA      255.24
    NES      236.99
    GB       234.88
    PS4      228.16
    Name: Global_Sales, dtype: float64
"""
print()
print(sales_by_platform.info())
"""
    <class 'pandas.Series'>
    Index: 31 entries, PS2 to PCFX
    Series name: Global_Sales
    Non-Null Count  Dtype  
    --------------  -----  
    31 non-null     float64
    dtypes: float64(1)
    memory usage: 496.0+ bytes
    None
"""
print()

# ---------------------------------------------------------
"""
    문제 6. 가장 많이 판매된 장르

    장르별 Global_Sales 총합을 구해 가장 높은 장르를 찾으시오.
"""
print(f"{'=' * 24} 가장 많이 판매된 장르 {'=' * 24}")
sales_by_genre = (df.groupby("Genre")["Global_Sales"]
                    .sum().sort_values(ascending=False))
print(sales_by_genre.head(1))
"""
    Genre
    Action    1167.99
    Name: Global_Sales, dtype: float64
"""
print()

# ---------------------------------------------------------
"""
    문제 7. Publisher 별 평균 판매량

    Publisher 별 평균 Global_Sales를 구하고, 상위 10개만 출력하시오.
"""
print(f"{'=' * 20} Publisher별 평균 판매량 Top 10 {'=' * 20}")
sales_mean_by_publisher = (df.groupby("Publisher")["Global_Sales"]
                             .mean().sort_values(ascending=False))
print(sales_mean_by_publisher.head(10))
"""
    Publisher
    Palcom                                4.170000
    Red Orb                               2.620000
    Nintendo                              2.562264
    Arena Entertainment                   2.360000
    UEP Systems                           2.250000
    RedOctane                             2.170000
    Sony Computer Entertainment Europe    1.768333
    Valve                                 1.740000
    Hello Games                           1.600000
    Westwood Studios                      1.550000
    Name: Global_Sales, dtype: float64
"""
print()

# ---------------------------------------------------------
"""
    문제 8. Publisher 별 가장 많이 발매한 장르

    각 Publisher가 가장 많이 만든 장르는 무엇인지 구하시오.
    (Publisher 별로 Genre count의 최댓값 찾기)
    [hint] groupby(['Publisher', 'Genre']).size().reset_index()
"""
print(f"{'=' * 20} Publisher별 최다 발매 장르 {'=' * 20}")

# df의 데이터를 Publisher로 그룹화 한 후, 다시 Genre로 세부 그룹화
# => 제작사_장르 그룹에 각각 size() 함수를 호출하여 행 수를 계산,
#    (Publisher, Genre)라는 멀티 인덱스 형태로 묶인 시리즈 데이터 반환
# => reset_index()를 호출하여 멀티인덱스 형태였던 Publisher, Genre를
#    다시 일반 컬럼으로 끌어올리기.
#    "개수(Count)"라는 새로운 컬럼을 가진 df 구조로 변환
publisher_genre_counts = (df.groupby(["Publisher", "Genre"])
                         .size().reset_index(name="Count"))
# 행 개수 확인용
print(f"제작사: 총 {df['Publisher'].nunique()}개")
"""
    제작사: 총 578개
"""

"""
    방법1: sort_values와 drop_duplicates() 활용
"""
# 개수 컬럼을 가진 df를 개수 내림차순 정렬
publisher_genre_max = publisher_genre_counts.sort_values("Count", ascending=False)
# 제작사별로 개수가 가장 큰 첫 번째 행 하나만 남기기 위해 중복 제거
publisher_genre_max = (publisher_genre_max
                       .drop_duplicates(subset=["Publisher"], keep="first"))
print(publisher_genre_max)
"""
                            Publisher         Genre  Count
    509                Electronic Arts        Sports    212
    1113            Namco Bandai Games        Action    203
    910   Konami Digital Entertainment        Sports    192
    1414   Sony Computer Entertainment          Misc    121
    83                      Activision        Action    112
    ...                            ...           ...    ...
    1818                   id Software       Shooter      1
    1817                          iWin        Puzzle      1
    1816                        fonfun    Simulation      1
    886                   Kids Station     Adventure      1
    1821          inXile Entertainment  Role-Playing      1

    [578 rows x 3 columns]
"""
print()
"""
    방법2: 조건부 인덱싱 활용
"""
# 개수 컬럼을 가진 df를 제작사별로 그룹화 한 후, 개수 컬럼을 기준으로,
# 집계함수 max를 활용하여 제작사별 최대 개수 컬럼 추가
max_counts = publisher_genre_counts.groupby("Publisher")["Count"].transform("max")
# 실제 개수가 해당 제작사의 최대 개수와 같은 행만 추출
publisher_genre_max = (publisher_genre_counts
                       [publisher_genre_counts["Count"] == max_counts]
                       # 장르별로 게임을 하나씩만 발매했을 수 있으므로 중복 제거
                       .drop_duplicates(subset=["Publisher"], keep="first"))
print(publisher_genre_max)
"""
                            Publisher         Genre  Count
    0                  10TACLE Studios     Adventure      1
    3                       1C Company        Racing      1
    6     20th Century Fox Video Games        Action      4
    8                           2D Boy        Puzzle      1
    9                              3DO        Action     14
    ...                            ...           ...    ...
    1818                   id Software       Shooter      1
    1819               imageepoch Inc.     Adventure      1
    1821          inXile Entertainment  Role-Playing      1
    1822                     mixi, Inc        Action      1
    1823                  responDESIGN        Sports      1

    [578 rows x 3 columns]
"""
print()

# ---------------------------------------------------------
"""
    문제 9. 국가별로 인기 있는 장르

    NA / EU / JP 각각 판매량이 가장 높은 장르를 구하시오.
"""
print(f"{'=' * 24} 국가별 인기 장르 {'=' * 24}")
# NA_Sales 최다 판매 장르
na_genre_sales = df.groupby("Genre")["NA_Sales"].sum()
print(f"NA_Sales 최다 판매 장르: {na_genre_sales.index[na_genre_sales.argmax()]}"
      f" ({na_genre_sales.max()*10_000:,.0f} 장)")
#EU_Sales 최다 판매 장르
eu_genre_sales = df.groupby("Genre")["EU_Sales"].sum()
print(f"EU_Sales 최다 판매 장르:{eu_genre_sales.index[eu_genre_sales.argmax()]}"
      f" ({eu_genre_sales.max()*10_000:,.0f}장)")
# JP_Sales 최다 판매 장르
jp_genre_sales = df.groupby("Genre")["JP_Sales"].sum()
print(f"JP_Sales 최다 판매 장르: {jp_genre_sales.index[jp_genre_sales.argmax()]}"
      f" ({jp_genre_sales.max()*10_000:,.0f}장)")
"""
    NA_Sales 최다 판매 장르: Action (5,720,300 장)
    EU_Sales 최다 판매 장르:Action (3,320,200장)
    JP_Sales 최다 판매 장르: Role-Playing (3,351,200장)
"""
print()
