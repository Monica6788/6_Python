"""
    점검하기

    데이터 정제 전에 데이터가 정상인지 여부를 확인하는 단계 (방법)
"""
import pandas as pd
from utils.config import RAW_PATH, ENCODING

# 인코딩 외의 옵션 없이 그대로 데이터 읽어오기
df = pd.read_csv(RAW_PATH, encoding=ENCODING)

print(f"형태(행, 열) df.shape : {df.shape} / {df.shape[0]}행 {df.shape[1]}열\n")

print(f"{'=' * 20} 상위 3개 데이터 조회 {'=' * 20}")
print(f"{df.head(3)}\n")
print(f"{'=' * 20} 열별 데이터 타입 확인 {'=' * 20}")
print(f"{df.dtypes}\n")

"""
    close, volume은 숫자(int)여야 하는데, 문자열(str)로 확인됨
    
    read_csv는 열마다 타입을 추론하는데, 한 열에 숫자가 아닌 값이
    "단 하나라도" 존재하면 그 열은 전체가 문자열로 판단됨!
"""
print(f"{'=' * 20} 현재 상태에서 통계 조회 {'=' * 20}")
print(f"{df[['close', 'volume', 'high', 'low']].describe()}\n")
"""
                high            low
    count   92721.000000   92721.000000
    mean    47259.797468   45291.619633
    std     62362.809455   59738.975017
    min      1973.000000    1915.000000
    25%     12341.000000   11847.000000
    50%     25530.000000   24453.000000
    75%     54755.000000   52472.000000
    max    591099.000000  567670.000000
"""
# int64 타입인 high, low 컬럼만 정상적으로 값이 출력되고,
# str 타입인 close, volume 컬럼은 값이 출력되지 않음

# df.info() : 행 수, 열 이름, non-null 개수, dtype을 출력
df.info()
print()
"""
    <class 'pandas.DataFrame'>
    RangeIndex: 92721 entries, 0 to 92720
    Data columns (total 9 columns):
    #   Column      Non-Null C0ount  Dtype  
    ---  ------      --------------  -----  
    0   code        92721 non-null  str    
    1   date        92721 non-null  str    
    2   open        92721 non-null  int64  
    3   high        92721 non-null  int64  
    4   low         92721 non-null  int64  
    5   close       92082 non-null  str         다른 컬럼들에 비해
    6   volume      87464 non-null  str         현저히 적은 non-null
    7   change      92721 non-null  int64  
    8   changeRate  92721 non-null  float64
    dtypes: float64(1), int64(4), str(4)
    memory usage: 6.4 MB
"""
# non-null 개수를 통해 전체 행 수와 다르면 결측이 있다고 판단함

# 결측률
#       df.isnull() / df.isna()
na = df.isnull().sum()
print(f"{'열':<14}{'결측 수':<14}{'결측률':<14}")
for col in df.columns:
    if na[col] > 0:
        print(f"{col:<14}{na[col]:<14}{na[col] * 100 / len(df):>9.2f}")
print()

# read_csv는 일부 문자열에 대해 자동으로 결측으로 변경해줌.
#   데이터에 N/A라고 되어 있는 값을 읽을 때 NaN이 됨.
#   다른 문자들은 전부 결측처리가 되지 않음.

# keep_default_na=False => 파일에 저장된 데이터를 그대로 읽어옴
#   dtype=str => 모든 열을 문자열로 읽어옴
#   ---> "N/A" 값을 자동으로 NaN으로 처리했던 기본값 작업을 하지 않고 문자열 그대로 읽어옴

df2 = pd.read_csv(RAW_PATH, encoding=ENCODING,
                  keep_default_na=False, dtype=str)
print(f"{'열':<14}{'N/A':>10}{'-':>10}{'빈칸':>10}")
for col in ['close', 'volume']:
    na_cnt = (df2[col] == "N/A").sum()
    dash_cnt = (df2[col] == "-").sum()
    blank_cnt = (df2[col] == "").sum()

    print(f"{col:<14}{na_cnt:>10}{dash_cnt:>10}{blank_cnt:>10}")


# 동일한 데이터가 오염되어 있어도 N/A은 결측으로 확인이 되는데, 
#    오염된 데이터가 확실하게 확인하기가 어려움!
# 데이터를 읽어올 때 결측으로 판단할 값들을 지정할 수 있음!
#  => na_values=['N/A', '-', ''] 옵션을 통해 결측 처리를 할 수 있음!!
"""위 아래 주석 동일한 내용임"""
# [문제점] 동일한 데이터 안에 "N/A"나 "-" 등 이상한 문자열이 섞여 있을 경우
#          Pandas가 이것을 진짜 결측치라고 알아채지 못하므로 일일이 찾아내기 어려움.
# [해결책] 파일을 읽어올 때부터 결측치로 처리할 문자열을 지정하면 됨.
#       => na_values=['N/A', '-', ''] 옵션 지정을 통해 결측 처리가 가능함
print()

# value_counts() : 어떤 값이 몇 번 나오는지 확인
#   - dropna=False: 결측치(NaN)도 하나의 값으로 처리
print(f"{df['close'].value_counts(dropna=False).head()}\n")

# 종가(close) 데이터의 경우, value_counts() 결과를 본다기보다는
#   오염된 데이터를 찾고자 할 때 이 방식으로 확인이 가능함 (dropna=False)

# to_numeric(errors="coerce") : 숫자로 변경 불가한 값에 대해 오류 대신 NaN으로 처리
for col in ['close', 'volume']:
    na_result = pd.to_numeric(df2[col], errors="coerce").isna().sum()
    print(f"{col:<10} : {na_result:>6} 건")
    # 콤마(,)가 포함된 데이터도 숫자로 변경불가인 값에 해당됨
print()

# 데이터 중복 확인
#   duplicate(subset=[기준열, 기준열, ...])
#   => 원본 길이와 같은 결과를 반환 (True/False)
#   => 첫 번째 값은 False, 두 번째부터 True

dup = df.duplicated(subset=['code', 'date']).sum()
print(f"(code, date) 중복 건수: {dup} 건\n")
print(f"중복 제거 후 개수 : {len(df) - dup} 건\n")

# 날짜 형식
#   --> 현재 실습 데이터에는 3가지 형식 존재

# 글자 수: .str.len()
lens = df['date'].astype(str).str.len().value_counts()
# print(lens)
# 2026-09-18,2026.09.18 --> 10글자
# 20260918 --> 8글자
print(f"20260918 형식: {lens.get(8, 0)}\n")     # 없으면 기본값 0

# 패턴 검색: .str.contains(keyword)
dot_cnt = df['date'].astype(str).str.contains(r"\.", regex=True).sum()
print(f"2026.09.18 형식: {dot_cnt} 건")
print(f"2026-09-18 형식: {lens.get(10, 0) - dot_cnt} 건")

temp = df.copy()
temp['date'] = pd.to_datetime(temp['date'], format="mixed")
dup2 = temp.duplicated(subset=['code', 'date']).sum()
print(f"날짜 데이터 변환 후 중복 건수: {dup2} 건")

print(f"날짜 형식 차이로 숨겨진 중복: {dup2 - dup}\n")
# G0001, 2026-09-18 / G0001, 20260918과 같은 데이터가 있으면 차이가 발생할 수 있다.

temps = pd.DataFrame({
    'code': ['G0001', 'G0001', 'G0002'],
    'date': ['2026-09-18', '20260918', '2026-09-18'],
    'close': [24_000, 24_000, 28_800]
})
print(temps)
print()
print(f"문자열인 상태에서 중복: {temps.duplicated(subset=['code', 'date']).sum()} 건")
temps['date'] = pd.to_datetime(temps['date'], format='mixed')
print(f"날짜 타입으로 변환 후 중복: {temps.duplicated(subset=['code', 'date']).sum()} 건\n")

# 어떤 데이터가 문제가 있는지 진단
#      => 타입 -> 중복 -> 결측 -> 이상치 -> 검증

# 데이터 정제 목표 정하기
print(f"{'항목':<24}{'현재':<14}{'목표':<14}")
print("-" * 54)
print(f"{'행 수':<24} {len(df):<14} {'90,000':<14}")
print(f"{'종목 수':<24} {df['code'].nunique():<14} {'120':<14}")
print(f"{'종목별 행 수 (최소~최대)':<18}"
      f"{str(df.groupby('code').size().min()) + '~'}" 
      f"{str(df.groupby('code').size().max()):<14}"
      f"{'750':<14}")

