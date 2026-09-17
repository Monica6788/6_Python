"""
    조회하기
"""
from utils.loader import load_csv
print(f"{'=' * 34} 파일 조회 {'=' * 34}")
df = load_csv()
print(df.head())
print()

# nunique() : 중복 제거한 후의 개수
print(f"{len(df)} 행 / {df['code'].nunique()} 개 종목")

# 마지막 거래일 -> 거래일: date 컬럼의 최댓값(가장 최근 날짜)
last_day = df['date'].max()
print(f"마지막 거래일: {last_day}")

# 마지막 거래일의 기록: 거래일이 마지막 거래일과 일치하는 항목만 추출
last_history = df[df['date'] == last_day].reset_index(drop=True)
print(f"기준일: {last_day} / {len(last_history)} 개 종목")
# print(type(last_history))   # pandas.DataFrame => head() 사용 가능

print(f"{'=' * 31} 최근 거래내역 조회 {'=' * 31}")
print(last_history.head())
print()

# 특정 열을 선택하여 조회
print(f"{'=' * 33} 특정 열만 조회 {'=' * 33}")
# SQL: SELECT code, close, changeRate FROM prices
# Pandas: df[['code', 'close', 'changeRate']]
print(last_history[['code', 'close', 'changeRate']].head())
print()

# 대괄호 개수에 따른 결과 타입 (1개 / 2개)
one = last_history['close']         # Series (shape: (107,))
two = last_history[['close']]       # DataFrame (shape: (107, 1))

print(f"last_history['close'] -> {type(one).__name__} (shape: {one.shape})")
print(f"last_history[['close']] -> {type(two).__name__} (shape: {two.shape})")
print()

"""
    바깥 대괄호는 데이터프레임에서 조회하기(꺼내기) 위해 사용
    안쪽 대괄호는 "목록(List)"을 지정하기 위해 사용
"""

# 조건을 지정하여 조회하기
print(f"{'=' * 33} 조건으로 조회 {'=' * 33}")

# SQL: WHERE close > 100000
# Pandas: df[df['close'] > 100000]
exps = last_history[last_history['close'] > 100_000]
print(f"결과: {len(exps)} 건")
# to_string()이 있으면 데이터가 많아도 생략하지 않고 전부 보여줌. => 디버깅에 유용
print(exps[['code', 'close']].to_string())
# print(exps[['code', 'close']].to_string(index=False))   # 인덱스 없이 조회
print()

# True 값이 1로 나오도록 하여 sum() 함수로 개수 세어보고 확인하기
result = last_history['close'] > 100_000
print(f"결과: {result.sum()} 건")
print()

# 복수 조건으로 조회
print(f"{'=' * 31} 복수 조건으로 조회 {'=' * 31}")

# SQL: WHERE 조건1 AND 조건2 / WHERE 조건1 OR 조건2
# Pandas: df[(조건1) & (조건2)] / df[(조건1) | (조건2)]

# 기준 데이터: 마지막 거래일 기록
#   close > 5만 AND changeRate > 0
both_satisfied = last_history[(last_history['close'] > 50_000) &
                              (last_history['changeRate'] > 0)]
print(f"결과: {len(both_satisfied)} 건")
print(both_satisfied[['code', 'close', 'changeRate']].to_string())
print()

"""
        SQL                                     Pandas
    ORDER BY 컬럼               df.sort_values(컬럼, ascending=True/False )
    LIMIT 개수                  df.head(개수)
    DISTINCT 컬럼               df[컬럼].unique(): 결과 / df[컬럼].nunique(): 개수
    COUNT(*) .. GROUP BY ~      df[컬럼].value_counts()
    IN (...)                    df[컬럼].isin([...])
"""
print(f"{'=' * 23} 가장 비싼 3개 종목 {'=' * 23}")
# 내림차순 정렬 후 head(3)
df = last_history
top3 = df.sort_values("close", ascending=False).head(3)
print(top3[['code', 'close']])
print()

print(f"{'=' * 21} 가장 많이 오른 3개 종목 {'=' * 21}")
rise_top3 = df.sort_values("changeRate", ascending=False).head(3)
print(rise_top3[['code', 'close', 'changeRate']])
print()

print(f"{'=' * 21} 1민 ≤ 종가 ≤ 5만 종목 {'=' * 21}")
result = df[(df['close'] >= 10_000) & (df['close'] <= 50_000)]
print(f"조회 결과: {len(result)} 건")
# print(df['close'].between(10_000, 50_000))      # Series
result = df[df['close'].between(10_000, 50_000)]
print(f"조회 결과: {len(result)} 건")
print()

print(f"{'=' * 21} 종목 코드 'G0001', 'G0050', 'G0100'만 조회 {'=' * 21}")
result = df[df['code'].isin(['G0001', 'G0050', 'G0100'])]   # Series
print(f"조회 결과 : \n{result}")
print()

"""
    loc vs iloc : 행/열 선택(인덱싱) 및 범위 선택(슬라이싱)
    
     - loc (Label Location): 라벨 기반 선택
       df.loc[행_선택, 열_선택]
            - 행 선택: 인덱스 라벨 (숫자, 문자열, ...)
            - 열 선택: 컬럼 라벨 (열 이름, 문자열, ...)
            => 슬라이싱 시에 *끝 라벨이 포함됨*

     - iloc (Integer location): 정수(위치) 기반 선택
       df.iloc[행_선택, 열_선택]
            - 행 선택: 0부터 시작하는 위치 (숫자)
            - 열 선택: 0부터 시작하는 위치 (숫자)
            => 위치 기반으로 기존 슬라이싱과 동일! *끝 인덱스는 제외됨*
"""
print(f"{'=' * 30} loc 적용 {'=' * 30}")
print(df.loc[0:2])       # 3건
print()

print(f"{'=' * 30} iloc 적용 {'=' * 30}")
print(df.iloc[0:2])      # 2건
print()

# loc 방식은 행에 대한 조건 적용과 컬럼 선택이 가능
print(f"{'=' * 10} loc은 행에 대한 조건 적용과 컬럼 선택 가능 {'=' * 10}")
result = df.loc[df['close'] > 200_000, ['code', 'close', 'volume']].head(3)
print(result)
print()

# 인덱스 설정 (변경) : df.set_index(컬럼)
print(f"{'=' * 22} 인덱스 설정 변경 df.set_index(컬럼) {'=' * 22}")
indexed = df.set_index('code')
print(indexed.head())
# 지정한 컬럼('code'열)이 사라지고, code가 index가 됨.
print()

# 'G0001' 종목의 'close', 'changeRate'만 조회
print(f"{'=' * 22} G0001 {'=' * 22}")
G0001 = indexed.loc['G0001', ['close', 'changeRate']]
print(G0001)        # Series 형태
