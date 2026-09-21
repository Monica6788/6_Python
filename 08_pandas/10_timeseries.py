"""
    시계열 데이터
    : 시간의 흐름에 따라 분포된 데이터 (시간, 수치/데이터)
"""
import pandas as pd
from utils.loader import load_merged

pd.set_option("display.width", 140)

df = load_merged()

# one 변수에 G0001 종목 데이터만 저장
one = df[df["code"] == "G0001"].reset_index()
print(f"one index: {one.index}")

# 날짜 데이터를 인덱스로 사용
#   set_index(인덱스열): 지정한 열이 인덱스가 되어 새로운 df 반환
# one.info()
one = one.set_index('date').sort_index()
print(f"인덱스 변경 후 one index: {type(one.index)}")
print()

print(f"기간: {one.index.min().date()} ~ {one.index.max().date()}")
# one.index.date().min()은 오류 TypeError: 'numpy.ndarray' object is not callable
print()

# 문자열로 날짜 조회 가능
# 2026년 3월 전체 데이터 조회
print(f"26년 3월 전체: {len(one.loc['2026-03'])}행")
print(f"26년 1 ~ 6월 전체: {len(one.loc['2026-01':'2026-06'])}행")
# 날짜 인덱스로 슬라이싱 할 때는, 이전에 정렬이 되어 있어야 함. (sort_index())
print()

# dt 접근자
# 날짜 함수, 연/월/일 같은 조각을 꺼낼 때 사용
d = df.head(3)
print(f"연도: {d['date'].dt.year.tolist()}")
print(f"분기: {d['date'].dt.quarter.tolist()}")
print(f"요일: {d['date'].dt.dayofweek.tolist()}")

print(f"연/월로 변경: {d['date'].dt.to_period('M').astype(str).tolist()}")
print()

dow = df['date'].dt.dayofweek.value_counts().sort_index()
for k, v in dow.items():
    # '월화수목금토일'이라는 문자열의 k번째 인덱스에 해당하는 문자를 추출하여 요일 반환
    # dow 선언 시에 value를 value_counts()로 구해놔서 k-v의 v가
    # 해당 k의 건수가 됨.
    print(f"{'월화수목금토일'[k]}요일 {v:,}건")
print()

# resample: 시간 단위로 바꿔서 다시 묶어줌.
#   df.resample(시간단위).집계함수
#   => 시간 단위만큼의 행을 가진 결과. 뒤에 추가한 집계함수가 값을 정해줌.
#      시간 단위를 기준으로 한 groupby라고 볼 수 있다.
#      시간 단위: D(일), W(주), ME(월말), QE(분기말)

monthly_last = one['close'].resample('ME').last()
monthly_mean = one['close'].resample('ME').mean()
monthly_total_vol = one['volume'].resample('ME').sum()
print(f"{'월':<12} {'월말종가':<16} {'월평균가':<16}")
for idx in monthly_last.index[:4]:
    print(f"{idx.strftime('%Y-%m'):<12} {monthly_last[idx]:>16.0f} {monthly_mean[idx]:>16.0f}")

print(f"월간 총 거래량: {monthly_total_vol.iloc[0]:,.0f}건")
print()

# resample('ME').ohlc()
#   ohlc: Open(시가), High(고가), Low(저가), Close(종가)
#   => 기간별 시가, 고가, 저가, 종가 네개 열을 한 번에 만들 수 있음.
print(f"ohlc\n{one['close'].resample('ME').ohlc().head(3).round(0)}")
print()

# rolling: 연속된 N개 행을 윈도우 단위로 훑으면서 계산해주는 함수
#          이동 편균처럼 최근 N일 데이터가 필요할 때 사용
df = df.sort_values(['code', 'date']).reset_index(drop=True)

wrong = df['close'].rolling(20).mean()
# 람다식을 쓰는 이유
# : 종목별 경계를 지키면서 각 종목 안에서만 독립적으로 20일 이동평균을 구하기 위해
#   람다식 없이 rolling 사용 시 종목이 바뀔 때 두 종목의 데이터가 섞일 수 있음.
#   .transform(lambda s: ...)형태를 사용하면 각 종목별 그룹을 유지한 채 계산하고,
#   원본과 행 개수가 같은 결과로 돌려줌.
right = df.groupby('code')['close'].transform(lambda s: s.rolling(20).mean())
# lambda s: s.rolling(20).mean()
#   - s: 각 종목별 쪼개진 'close' 데이터 (Series)
edge = df.index[df['code'] != df['code'].shift()]
for i in [edge[1] - 1, edge[1], edge[1] + 1]:
    w = f"{wrong[i]:,.0f}" if pd.notna(wrong[i]) else "NaN"
    r = f"{right[i]:,.0f}" if pd.notna(right[i]) else "NaN"

    # df.loc[i, 'code']: i번째 행의 code 정보
    print(f"{i:<8} {df.loc[i, 'code']:<9} {df.loc[i, 'close']:>10,} {w:>20} {r:>20}")
print()

"""
groupby 없이 계산하면 (wrong의 경우) 종목별 코드가 달라도 이동평균선 재계산 없이
이어지는 형태로 계산된다.
=> 그룹화를 해줘야 종목별 20일 이평선이 정상적으로 계산됨.

diff, shift, rolling, ... 모두 groupby가 필요함!
"""

# 변화율 계산
# pct_change: 바로 윗행 대비 비율 변화
# cumprod: 누적곱
#   s.comrod(): s[0], s[0] * s[1], s[0] * s[1] * s[2], ...
df['ret'] = df.groupby('code')['close'].transform(lambda s: s.pct_change())
sample = df[df['code'] == 'G0001'].head(4)
for _, r in sample.iterrows():
    ret = f"{r['ret']:.4f}" if pd.notna(r['ret']) else 'NaN'
    print(f"{r['date'].date()} {r['close']:,} {ret}")

# 누적 수익률
# => 첫 날의 NaN을 0으로 채우고, (1 + 수익률)을 차례로 곱하기
cum = (df[df['code'] == 'G0001']['ret'].fillna(0) + 1).cumprod().iloc[-1]
print(f"G0001 종목의 누적 수익률: {(cum - 1) * 100:.1f} %")

