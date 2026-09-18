"""
    결측치 처리
"""
import pandas as pd

from utils.config import step_path

# _step2.pkl 파일을 읽어서 df 변수에 저장
df = pd.read_pickle(step_path('_step2.pkl'))
print(f"Step 2 : 이상치 처리 완료... {len(df)} 행")

print(f"{'=' * 20} 현재 결측 {'=' * 20}")
for col in ['open', 'high', 'low', 'close', 'volume']:
    n = df[col].isna().sum()

    if n:   # 0은 Falsy이므로 0이 아닐 때만 아래 블록이 실행됨
        print(f"{col}: {n} 건 ({100 * n / len(df):.2f} %)")

"""
    결측 처리 3가지 전략 (방법)
        - 삭제: dropna(subset=, how=, ...)
            => 삭제할 행 없이도 분석이 가능한지?
        - 대치: fillna(값/평균/중앙값)
            => 대푯값으로 적절한 것이 있는지?
        - 보간: interpolate()
            => 시계열 데이터. 앞뒤 값 사이를 이어줌!
"""

# 보간: 종목별로 처리해야 함!
# shift() 한 칸씩 옆으로 밀어줌.
"""
원본     ->   shift 데이터
0: A            0: NaN (밀려 내려올 데이터가 없어서 빈 칸이 됨)
1: B            1: A
2: B            2: B
3: C            3: C
...

edge = df.index[df['code'] != df['code'].shift()][1]
=> 현재 행의 종목 코드가 바로 윗줄의 종목 코드와 달라지는 인덱스들의 목록(배열)
=> [0, 750, 1500, ...]과 같이 나옴
=> [1]을 덧붙여서 두 번째 종목이 시작하는 위치를 가져온 것임
"""
edge = df.index[df['code'] != df['code'].shift()][1]
print(edge)

demo = df.loc[edge-2:edge+2, ['code', 'date', 'close']].copy()
print(demo)
print()

demo.loc[edge, 'close'] = pd.NA
demo['close'] = pd.to_numeric(demo['close'], errors='coerce')
print("-" * 60)
print(demo)
print()

result1 = demo['close'].interpolate()
print(result1)
"""
    NaN 처리했던 G0002의 데이터가 18547.0이 됨
    749번 인덱스의 G0001 9963.0과 751번 인덱스의 G0002 27131.0의 중점쯤으로 자동보정된 것

    근데 이제 종목 코드가 다른 항목인데 이러면 안 되므로 groupby()를 먼저!
"""
result2 = demo.groupby('code')['close'].transform(lambda s: s.interpolate())
print(result2)
print()

"""
    groupby 없이 보간 처리 시
        : 마지막 종가(G0001)와 뒷 종목의 다음 종가 사이를 이어버린다.
    groupby를 사용시
        : 보간처리를 하면 해당 종목(그룹화 기준열) 안에서만 이어준다.
"""
# 열별로 각각 다른 방법을 적용하여 처리
#   open, high, low, close => 종목 별로 보간 (시계열 데이터, 연속성)
#   volume => 결측 유지 (0으로 채우면 안됨)

OHLC = ['open', 'high', 'low', 'close']
before = df[OHLC].isna().sum().sum()
print(f"OHLC 결측: {before} 건")

for col in OHLC:
    df[col] = df.groupby('code')[col].transform(lambda s: s.interpolate())

pola = df[OHLC].isna().sum().sum()
print(f"종목 별 보간 처리 후 : {pola} 건")
# 종목의 맨 앞/뒤에 남은 결측 개수

# .ffill(): 결측을 바로 앞의 값으로 채움
# .bfill(): 결측을 바로 뒤의 값으로 채움

for col in OHLC:
    df[col] = df.groupby('code')[col].transform(lambda s: s.ffill().bfill())

fb = df[OHLC].isna().sum().sum()
print(f"ffill + bfill 처리 후 : {fb} 건")

# 거래량 (volume)은 결측 유지