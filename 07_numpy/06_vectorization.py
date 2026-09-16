"""
    벡터화 연산

    넘파이의 핵심 특징.
    반복문 없이 연산 수행 가능. (빠름)
"""
import numpy as np

from load_utils import load_dates, load_codes, load_one_stock

print(f"{'=' * 29} {'벡터화'} {'=' * 29}")
dates = load_dates()           # 거래일 배열
codes = load_codes()           # 종목 코드 배열
prices = load_one_stock(0)     # 첫 종목의 750일 종가

a = np.array([10,20,30,40])
b = np.array([1,2,3,4])
print(f"a: {a}\nb: {b}")
print(f"a * 2 = {a * 2}")       # [20 40 60 80]         
print(f"a + b = {a + b}")       # [11 22 33 44]
print(f"a > 25 = {a > 25}")     # [False False True True]
print()

# 유니버설 함수 (ufunc) : 배열의 모든 요소에 하나씩 적용되는 함수
print(f"{'=' * 27} {'유니버설 함수'} {'=' * 27}")
x = np.array([121, 144, 169, 196])
# sqrt(): 제곱근
print(f"x: {x}\nsqrt: {np.sqrt(x)}")

x = np.array([1.414213, 1.73205081, 2.23606, 2.6457513])
# round(배열, n): 소수점 아래 (n+1)번째 자리에서 반올림
print(f"x: {x}\nround(x, 3): {np.round(x, 3)}")

x = np.array([-1, 4, -9, 16])
# abs(배열): 절댓값
print(f"x: {x}\nabs(x): {np.abs(x)}")
print()

# 집계 함수
print(f"{'=' * 28} 집계 함수 {'=' * 28}")
print(f"{' ' * 24} {codes[0]} 750일 종가 {' ' * 25}")
print("-" * 67)
print(f"전체 합: {prices.sum():,} 원")
print(f"전체 평균: {prices.mean():,.0f} 원")
print(f"전체 표준편차: {prices.std():,.0f}")
print(f"최저가: {prices.min():,} 원")
print(f"최고가: {prices.max():,} 원")
print()

max_idx = prices.argmax()       # 가장 큰 값이 있는 위치 (인덱스)
min_idx = prices.argmin()       # 가장 작은 값이 있는 위치 (인덱스)

print(f"최고가: {prices[max_idx]:,} 원 ({dates[max_idx]})")
print(f"최저가: {prices[min_idx]:,} 원 ({dates[min_idx]})")
print()

"""
    수익률 (전일 대비 변화량) = (오늘금액 - 어제금액) / 어제금액

    prices[1:]: 둘째날부터 끝까지 (오늘)
    prices[:-1]: 첫 날부터 끝에서 두 번째 날까지 (어제)
"""
result = (prices[1:] - prices[:-1]) / prices[:-1]

print(f"일간 수익률: {len(result)} 건")
# TODO 왜 len(result)지...
print(f"평균: {result.mean() * 100:.2f}%")
print(f"표준편차: {result.std() * 100:.2f}%")
print(f"최대 상승: {result.max() * 100:.2f}% ({dates[result.argmax() + 1]})")
print(f"최대 하락: {result.min() * 100:.2f}% ({dates[result.argmin() + 1]})")
