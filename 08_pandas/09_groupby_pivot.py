"""
    groupby
    : split -> apply -> combine
        - split: 특정 열(키, 컬럼)을 기준으로 쪼개기
        - apply: 각 그룹에 함수를 적용
        - combine: 결과를 하나로 합치기
   
    pivot
"""
import pandas as pd
from utils.loader import load_merged

df = load_merged()
print(f"통합 데이터: {len(df)}행 / {df['code'].nunique()}종목 / {df['sector'].nunique()}섹터")
# agg: 요약표를 만들 때 그룹별로 결과를 도출
# transform: 원본에 열을 추가해서 값을 비교하고자 할 때,
#            그룹별로 계산 결과를 원본과 동일하게 도출
# filter: 그룹별로 검사해서 조건에 맞지 않으면 제외

# 종목 코드가 "G0001", "G0002"인 데이터만 추출하여 two 변수에 저장
# 혹시 모르니 인덱스 초기화까지
# two = df[(df["code"] == "G0001") | (df["code"] == "G0002")].reset_index(drop=True)
two = df[df["code"].isin(["G0001", "G0002"])].reset_index(drop=True)
print(f"{two[['code', 'date', 'close']].head(6)}\n")

# diff() : 바로 위 행과의 차이를 반환
#   s.diff() -> s[i] - s[i - 1] (맨 첫 행은 NaN)

wrong = two["close"].diff()
right = two.groupby("code")["close"].diff()

# shift() : 열을 통째로 한 칸 아래로 밀어줌
#    s.shift() -> 원본과 길이가 같은 Series를 반환
#                 i번째 값 = s[i - 1] (맨 첫 행은 NaN)

# "code"의 값이 달라지는 부분, 즉 G0001이 끝나고 G0002가 시작된 행의 인덱스 찾기
boundary = two.index[ two["code"] != two["code"].shift() ]
print(f"{boundary}")
print(f"종목이 바뀌는 지점: {boundary[1]}번째 행\n")
# [0] -> 첫 행. 이전 데이터가 없으므로 True
# [0] : 첫 행(인덱스 0). 이전 데이터와의 비교가 불가능하거나 첫 번째 종목의 시작지점.
# 두 번째 종목이 시작되는 경계 지점은 [1] 위치가 될 것임

for i in range(boundary[1] - 2, boundary[1] + 2):
    w = f"{wrong[i] if pd.notna(wrong[i]) else 'NaN'}"
    r = f"{right[i]}" if pd.notna(right[i]) else "NaN"

    # two.loc[i, 'code'] i번째의 code 정보
    print(f"{i:<8} {two.loc[i, 'code']:<9} {two.loc[i, 'close']:<12} {w:>20} {r:>20}")
print()

count_num = df.groupby("sector")["code"].count()
nunique_num = df.groupby("sector")["code"].nunique()

print(f"count: {count_num}")
print()
print(f"nunique: {nunique_num}")
print()

"""
    한 종목이 750 행이면 count는 750, nunique는 1
"""
# agg : 요약표
summary = df.groupby("sector").agg(
                종목수 = ("code", "nunique"),
                거래일수=("date", "count"),
                평균종가=("close", "mean"),
                최대거래량=("volume", "max")
)
print(summary.round())

# filter : 그룹 단위로 걸러내기. 조건을 만족하는 그룹 전체를 남겨준다.
#          SQL의 HAVING 절과 비슷한 역할을 해준다고 볼 수 있음.

# 거래일이 700일 미만인 종목 제외
filtered = df.groupby("code").filter(lambda g: len(g) >= 700)
print(f"{len(df)}행 {df['code'].nunique()}종목")
print(f"--> {len(filtered)}행 {filtered['code'].nunique()}종목")
# 전 종목에 750일짜리 데이터가 존재해서 걸러지는 것이 없음.
print()

# g["close"].mean() -> 750일의 종목 평균
# 종목 평균이 100_000 이하인 종목을 제외
# lambda g: g["close"].mean() > 100_000 
#       -> 이 그룹(g)의 "close"의 평균이 10만을 초과
big = df.groupby("code").filter(lambda g: g["close"].mean() > 100_000)
print(f"{len(big)}행 {big['code'].nunique()}종목")
print()

"""
    filter를 사용하면 특정 행이 아닌 그룹 전체를 남기거나 버림

    조건에 맞는 행만 남기고자 할 경우?
        => df[df['close'] > 100_000]
"""

# 다중 그룹, MultiIndex
multi = df.groupby(["sector", "market"])["close"].mean()
print(f"인덱스 타입: {type(multi.index).__name__}") # 인덱스 타입: MultiIndex
print(multi.head(6).round(0))
# 여러 개(n개)의 열을 기준으로 그룹화를 하면, 인덱스가 n개인 시리즈로 반환됨

print("========== 인덱스의 첫 번째 레벨로 조회 (sector) ==========")
print(multi.loc['금융'].round(0))
print()

print("==== 인덱스의 모든 레벨을 지정하여 조회 -> 튜플로 전달 ====")
print(multi.loc[('금융', 'GX-GROWTH')])
print()

"""
    ========== 인덱스의 첫 번째 레벨로 조회 (sector) ==========
    market
    GX-GROWTH    21276.0
    GX-MAIN      55938.0
    Name: close, dtype: float64

    ==== 인덱스의 모든 레벨을 지정하여 조회 -> 튜플로 전달 ====
    21276.007619047617
"""

# unstack() : 인덱스를 열로 펼침
print(multi.unstack())
print()
"""
    market      GX-GROWTH       GX-MAIN
    sector                             
    IT서비스    42249.549333  70299.538476
    건설       13167.793333  51956.698933
    금융       21276.007619  55938.200970
    바이오      24106.959556  71050.116593
    식품      106389.572889  19357.816444
    에너지      15653.564889   9517.631333
    운수장비     25057.412267  41723.037333
    유통       12091.581667  75796.127667
    전기전자     12738.016762  72112.403111
    화학       19819.189778  67319.463259
"""
# 인덱스의 안쪽 레벨 값을 열로 올려줌.
#   => 세로로 길게 늘어졌던 형태를 표 형태로 바꾸어주는 것.

# reset_index(): 인덱스를 열로 되돌림
print(multi.reset_index().head(3).round(0))
"""
    sector     market    close
    0  IT서비스  GX-GROWTH  42250.0
    1  IT서비스    GX-MAIN  70300.0
    2     건설  GX-GROWTH  13168.0
"""
# 인덱스 값이 열이 되고, 인덱스는 0, 1, 2, ...으로 새로 만들어짐.

# groupby(... as_index=False):처음부터 그룹화 기준이 열로 나옴
flat = df.groupby(['sector', 'market'], as_index=False)['close'].mean()
print(flat.columns.tolist())
"""
    sector     market    close
    0  IT서비스  GX-GROWTH  42250.0
    1  IT서비스    GX-MAIN  70300.0
    2     건설  GX-GROWTH  13168.0
    ['sector', 'market', 'close']
"""
print()

# 피벗 - 형식 바꾸기
"""
    pivot_table: 한 열은 행으로, 다른 열은 열로 펼쳐서 집계
        df.pivot_table(index=기준행, columns=기준열, values=집계대상열, aggfunc=집계함수)
            - 기준행: 행 기준이 될 열
            - 기준열: 열 기준이 될 열
            - values: 집계대상이 될 열
            - aggfunc: 집계 함수
"""
d = df.copy()

# 분기 정보 추가
d['quarter'] = d['date'].dt.to_period("Q").astype(str)
# to_period(): 날짜를 기간으로 변경 (Q: 분기, M: 월, Y: 연)

pv = d.pivot_table(
    index="sector",      # 행
    columns="quarter",   # 열
    values="close",      # 셀 데이터 (연산대상)
    aggfunc="mean"       # 셀 데이터 집계 함수
)

print(pv.iloc[:5, :4].round(0))
"""
quarter   2023Q3   2023Q4   2024Q1   2024Q2
    sector                                     
    IT서비스    62969.0  65508.0  69180.0  64702.0
    건설       32757.0  34405.0  31417.0  27326.0
    금융       45454.0  45893.0  49738.0  51253.0
    바이오      79691.0  84871.0  72333.0  60830.0
    식품       56101.0  49774.0  38671.0  42945.0
"""
print()

# 넓은 형식과 긴 형식
wide = pv.iloc[:3, :3]
print(f"{'=' * 20} 넓은 형식 pivot {'=' * 20}")   # 사람이 보기 편함
print(wide.round())
"""
    ==================== 넓은 형식 pivot ====================
    quarter   2023Q3   2023Q4   2024Q1
    sector                            
    IT서비스    62969.0  65508.0  69180.0
    건설       32757.0  34405.0  31417.0
    금융       45454.0  45893.0  49738.0
"""
# 사람이 보는 보고서, 엑셀, 데이터 확인 시 활용
print()

# melt: 넓은 형식을 긴 형식으로 녹여서 표현
#       즉 넓은 형식 -> 긴 형식: 피벗의 정반대 작업
#   df.melt(id_vars=유지할_열, var_name=열이름을_담을_열, value_name=값을 담을 열)
#   => 열마다 흩어져 있는 값을 하나의 열에 모으기 위함.
long = wide.reset_index().melt(id_vars="sector", var_name="quarter", value_name="close")
#      가로로 펼쳐져 있던 열 이름들을 하나의 열(여기서는 quarter)로 모으고,
#      값들을 밸류 열(여기서는 close)로 내린다.
print(f"{'=' * 21} 긴 형식 melt {'=' * 21}")
print(long.head(6).round())
"""
    ===================== 긴 형식 melt =====================
    sector quarter    close
    0  IT서비스  2023Q3  62969.0
    1     건설  2023Q3  32757.0
    2     금융  2023Q3  45454.0
    3  IT서비스  2023Q4  65508.0
    4     건설  2023Q4  34405.0
    5     금융  2023Q4  45893.0
"""
# DB 저장, 시각화할 때 활용
print()

# pivot 함수를 사용하여 긴 형식을 넓은 형식으로 바꿀 수도 있음.
# index (행 기준): 생성할 피벗 테이블에서 행의 축이 될 열 지정
#                  index에 지정된 열의 고유값들이 새로운 df의 행 이름(index)로 배치됨
# columns (열 기준): 생성할 피벗 테이블에서 열의 축이 될 열 지정.
#                    가로 방향의 새로운 컬럼 이름 (Header)으로 배치됨
# values (셀 데이터): 실제 표의 제목행, 열 부분 말고 데이터로 채워지는 부분 지정
#                     섹터 행과 분기 열이 만나는 셀 안에 해당 데이터가 배치됨.
back = long.pivot(index="sector", columns="quarter", values="close")
print(back.round())