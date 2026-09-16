"""
    넘파이 배열 생성
"""
import numpy as np
from load_utils import load_one_stock

print(f"{'=' * 28} {'배열 생성'} {'=' * 28}")
print(f"리스트를 배열로 생성 : {np.array([600_000, 25_000, 42_800])}")
print(f"0으로 채워서 배열로 생성 (타입 기본값 float) : {np.zeros(5)}")
print(f"0으로 채워서 배열 생성 (타입 지정) : {np.zeros(5, dtype='int64')}")
print(f"1로 채워서 배열 생성 (타입 기본값 float) : {np.ones(5)}")
print(f"1로 채워서 배열 생성 (타입 지정) : {np.ones(5, dtype='int64')}")
# np.full(개수, 채울값)
print(f"특정 값으로 채워서 배열 생성 : {np.full(5, 7)}")
print(f"0부터 9까지의 정수 배열 생성 : {np.arange(10)}")
print(f"0부터 100까지 5등분점의 배열 생성 : {np.linspace(0, 100, 5)}")
print()

print(f"{'=' * 30} {'속성'} {'=' * 30}")

arr = np.array([12_300, 44_400, 1_779_000])
print(f"arr : {arr}")
print(f"배열 형태 (shape) : {arr.shape}")                # 튜플 (3,)
print(f"차원 수 (ndim) : {arr.ndim}차원")                # 1차원
print(f"데이터 개수 (size) : {arr.size}개")              # 3개
print(f"데이터 (요소) 타입 (dtype) : {arr.dtype}")       # int64
print()
"""
    shape 해석
    (n,)        -> 1차원 배열 (n열)
    (n, m)      -> 2차원 배열 (n행 m열)
        ex. (4, 1) : 4행 1열    / (1, 4) : 1행 4열
    (x, y, z)   -> 3차원 배열 (x면 y행 z열)
"""
print(f"{'=' * 29} {'reshape'} {'=' * 29}")
# (4,) : 1차원 배열 ex. array([1, 2, 3, 4])
# (4, 1) : 2차원 열 벡터 ex. array([ [1], [2], [3], [4] ])
# (1, 4) : 2차원 행 벡터 ex. array([ [1, 2, 3, 4] ])
for shape in [(4,), (4, 1), (1, 4)]:
    # np.arange(4) -> [0 1 2 3]
    a = np.arange(4).reshape(shape)

    print(f"shape: {str(shape)} / ndim: {a.ndim} / {a}")
    # shape: (1, 4) / ndim: 2 / [[0 1 2 3]]
print()
print("-" * 60)

# 첫 번째 종목의 데이터 불러오기
print(f"{'=' * 28} {'1번 종목'} {'=' * 28}")
prices = load_one_stock(0)

print(f"첫 종목의 750일 종가")
print(f"앞의 5개 데이터 : {prices[:5]}")    # [24015 24400 24295 23974 23784]
print(f"shape : {prices.shape}")            # (750,)
print(f"ndim : {prices.ndim}")              # 1
print(f"dtype: {prices.dtype}")             # int64

