"""
    Pandas 판다스

    Numpy(넘파이) 기반의 데이터 구조를 제공하고,
    SQL처럼 다양한 조작 및 분석 기능을 제공하는 라이브러리
"""
import pandas as pd
from utils.config import RAW_PATH, ENCODING, path

"""
    # Series (시리즈) : 라벨링 된(이름이 붙여진) 1차원 배열 구조
      - 인덱스(라벨)를 따로 지정하지 않으면 정수로 자동 생성됨 (0 ~ )
"""
datas = [10, 20, 30, 40]
# 시리즈 생성
s = pd.Series(datas)
print(s)
print()
"""
인덱스      데이터
0           10
1           20
2           30
3           40
dtype: int64
"""

# 인덱스 정보
print(f"{'=' * 26} 인덱스 정보 .index {'=' * 26}")
print(f"index: {s.index} / {s.index.to_list()}")
# index: RangeIndex(start=0, stop=4, step=1) 0부터 3(4 직전)까지, 1 간격.
# [0, 1, 2, 3] 인덱스 리스트
print()

# 실제 저장된 데이터
print(f"{'=' * 25} 데이터 정보 .values {'=' * 25}")
# 이름(객체의 타입명)만 확인하기 위해 던더 속성 __name__ 호출
print(f"values: {s.values} ({type(s.values).__name__})")
# values: [10 20 30 40] (ndarray)
print()

# name: 시리즈의 이름, 데이터프레임 생성 시 열 이름으로 사용됨.
print(f"{'=' * 30} name 속성 {'=' * 30}")
print("시리즈의 이름. 데이터프레임 생성 시 열 이름으로 사용됨.")
s = pd.Series(datas, name="sameple")
print(s)
print(f"name: {s.name}")
print(f"index: {s.index}")
print(f"values: {s.values}")
print()

# 인덱스 지정
s = pd.Series(datas, index=['a', 'b', 'c', 'd'])
print(s)
print(f"index: {s.index}")
"""
인덱스      데이터
0           10
1           20
2           30
3           40
dtype: int64
index: Index(['a', 'b', 'c', 'd'], dtype='str')
"""
print()

s1 = pd.Series([10, 20, 30], index=['x', 'y', 'z'])
s2 = pd.Series([1, 2, 3], index=['z', 'y', 'x'])

print("* s1")
print(s1)
print()

print("* s2")
print(s2)
print()

print(f"* s1 + s2\n{s1 + s2}") # x = 13, y = 22, z = 31
# 연산이 수행될 때 순서가 아닌 인덱스를 기준으로 연산이 수행됨
#   -> 인덱스가 같은 것끼리 연산

s3 = pd.Series([1, 2], index=['x', 'w'])
print("* s3")
print(s3)
print()

print(f"* s1 + s3\n{s1 + s3}")
"""
* s1 + s3
w     NaN
x    11.0
y     NaN
z     NaN
dtype: float64
"""
# 연산이 수행될 때 동일한 인덱스가 없으면 연산 결과는 NaN이 된다.
print()

"""
    # DataFrame (데이터프레임): 2차원 테이블 구조
      - Series를 여러 개 묶어 만든 2차원 구조
      - 행(인덱스)과 열(컬럼)로 구성
"""
wanna_eat = {
    "이름": ["과자", "떡볶이", "케이크"],
    "가격": [2000, 4000, 6800],
    "재고": [10, 5, 8],
}

# DataFrame 생성
df = pd.DataFrame(wanna_eat)
print(df)
"""
    이름    가격  재고
0   과자  2000  10
1  떡볶이  4000   5
2  케이크  6800   8
"""
print()

# dtypes: 각 열의 데이터 타입을 확인할 수 있는 속성
print(f"dtypes: \n{df.dtypes}")
"""
dtypes: 
이름      str
가격    int64
재고    int64
dtype: object
"""
# shape: 행과 열의 개수를 확인할 수 있는 속성
print(f"shape: {df.shape}")
# shape: (3, 3)

# index: 행 인덱스를 확인할 수 있는 속성
print(f"index: {df.index}")
# index: RangeIndex(start=0, stop=3, step=1)

# columns: 열 이름(컬럼명)을 확인할 수 있는 속성
print(f"columns: {df.columns}")
# columns: Index(['이름', '가격', '재고'], dtype='str')

print()

# 파일로부터 읽어와서 생성
print(f"{'=' * 30} 파일로 읽어와서 생성 {'=' * 30}")
# CSV (Comma Separated Values) : 콤마(쉼표)로 구분되어 있는 데이터
# pd.read_csv(파일명) => DataFrame
df = pd.read_csv(RAW_PATH, encoding=ENCODING)

print(df.head())        # 위에서부터 5개의 데이터 조회
print()

print(f"close(종가) 컬럼의 dtype: {df['close'].dtype}")     # str
print(f"date(날짜) 컬럼의 dtype: {df['date'].dtype}")       # str

# read_csv는 열마다 타입을 추론하는데,
#   한 열에 숫자가 아닌 값이 하나라도 있으면 그 열은 문자열로 읽음
# => 옵션을 추가하면 좀 더 명확하게 타입을 추론해서 가져올 수 있음.

print("-" * 82)
print(f"{'=' * 30} 옵션을 추가하여 생성 {'=' * 30}")
df = pd.read_csv(RAW_PATH,
                 encoding=ENCODING,
                 parse_dates=["date"],      # 'date' 열은 datetime으로 처리
                 na_values=["N/A", "-"],    # 결측으로 취급할 문자열들
                 thousands=",")             # '1,000,000' 형태를 숫자로 처리
print(df.head())
print()

print(f"close(종가) 컬럼의 dtype: {df['close'].dtype}")     # float64
print(f"date(날짜) 컬럼의 dtype: {df['date'].dtype}")       # str
print()

print(f"date unique (중복제거한 결과): {df['date'].unique()}")
print()
# '-'로 구분되지 않은 형태(20231003, 2024.11.26 등)가 섞여 있음

# date 열에는 2026-09-17, 20260917, 2026.09.17 형태들로 섞여 있음.
#   parse_dates 옵션은 해당 열 전체가 같은 형식일 때만 적용됨.
#   형식이 섞여 있을 경우 별도로 처리해줄 필요가 있음 => to_datetime() 사용

df['date'] = pd.to_datetime(df['date'], format="mixed")
print(f"to_datetime -> {df['date'].dtype}")
print()

"""
    read_csv의 옵션

     - encoding: utf-8 / utf-8-sig
     - parse_dates: 특정 열(날짜)을 datetime으로 변환
     - na_values: 결측으로 취급할 문자열 지정
     - thousands: 천 단위 구분자 제거 (천 단위 구분자(콤마 등)가 있는 데이터를 숫자로 변환)
"""
# 데이터를 불러온 후 점검하기
#   df.head(n): 위에서부터 n개의 데이터를 조회 (생략 시 기본값 5개)
print(df.head(3))
print()

#   df.shape: 불러온 데이터의 행, 열 개수
print(df.shape)
print()

#   df.info(): 불러온 데이터의 컬럼별 데이터 개수, 타입 등을 확인
df.info()
"""
    <class 'pandas.DataFrame'>
    RangeIndex: 92721 entries, 0 to 92720
    Data columns (total 9 columns):
    #   Column      Non-Null Count  Dtype         
    ---  ------      --------------  -----         
    0   code        92721 non-null  str           
    1   date        92721 non-null  datetime64[us]
    2   open        92721 non-null  int64         
    3   high        92721 non-null  int64         
    4   low         92721 non-null  int64         
    5   close       91619 non-null  float64       
    6   volume      87025 non-null  float64       
    7   change      92721 non-null  int64         
    8   changeRate  92721 non-null  float64       
    dtypes: datetime64[us](1), float64(3), int64(4), str(1)
    memory usage: 6.4 MB
"""
print()

#   df.dtypes: 컬럼별 데이터 타입
print(df.dtypes)

