"""
    불리언 인덱싱과 마스킹
"""
import numpy as np

from load_utils import load_matrix, load_column

arr = np.array([10, 25, 30, 15, 40])
mask = arr > 20

print(f"arr: {arr}")
print(f"arr > 20: {mask}")

# mask 자체를 인덱스로 사용하면 True에 해당하는 값만 확인 가능
# 대괄호 안에 mask(조건 수행 결과 리스트)를 넣으면,
# True에 해당하는 위치 값들만 배열로 만들어 줌.
print(f"arr[mask]: {arr[mask]}")
# mask의 합계 = True의 개수
print(f"True 개수: {mask.sum()}개")
print()

matrix = load_matrix()
big = matrix > 500_000
print(f"matrix > 500,000: shape {big.shape} / dtype {big.dtype}")
print(f"True의 개수: {big.sum()}개 / 전체: {matrix.size:,}개")

print(f"{matrix[big].shape}")   # (115,)
# 2차원 배열에 불리언 인덱싱을 하면 1차원 배열이 추출된다.
print()

# np.diff(배열, axis=1): 인접한 두 요소의 차를 계산 (오른쪽 값 - 왼쪽 값)
#   axis=1이면 같은 행에서 열 방향으로 차(-)를 구함
#   결과 (120, 749)
result = np.diff(matrix, axis=1)    # 일간 수익률
print(result)

cond1 = result > 0.03              # 일간 수익률 3% 초과

# 거래량 (volume)
# 행(콤마 전 부분)은 처음부터 끝까지, 열(콤마 뒷부분)은 1번부터 끝까지
volumes = load_column("volume")[:, 1:]     # (120, 750) -> (120, 749)
cond2 = volumes > 2_000_000                # 거래량이 200만 주(건) 초과

# and --> & or --> | not --> ~
intersection = cond1 & cond2
print(f"(일간 수익률 > 3%) ∩ (거래량 > 2M) : {intersection.sum()}")
print(f"일간 수익률 <=  3%인 건수 : {(~cond1).sum()}")
print()

sample1 = np.array([0.05, -0.02, 0.0, 0.12, -0.15])
sample2 = np.where(sample1 > 0, "up",
         np.where(sample1 < 0, "down" , "keep"))
print(sample2)


