"""
    결측과 이상치
"""
import numpy as np
from load_utils import load_dirty

arr, nan_idx, outlier_idx = load_dirty()

print(f"{'=' * 28} np.nan {'=' * 28}")
print(f"np.nan == np.nan : {np.nan == np.nan}")     # False
print(f"np.nan != np.nan : {np.nan != np.nan}")     # True
print(f"np.nan > 1 : {np.nan > 1}")                 # False
print(f"np.nan <= 1 : {np.nan <= 1}")               # False
print(f"np.nan + 1 : {np.nan + 1}")                 # nan
print()

# nan의 의미가 not a number이므로,
# "모름"과 "모름"을 비교하거나 연산을 수행했을 때 결과를 알 수 없음

result = (arr == np.nan)
print(f"arr == np.nan : {result.sum()}개")      # 0 즉 전부 False 
#   => 동등 비교로 결측치를 찾을 수 없음

result = np.isnan(arr)
print(f"총 개수: {len(arr)}개 / 결측: {result.sum()}개")
print(f"결측치의 위치 : {np.where(result)[0]}")
# _NAN_IDX와 동일
# [37, 88, 142, 199, 242, 301, 358, 412, 470, 537, 618, 703]

print(f"평균: {np.mean(arr)} -> {np.nanmean(arr):.2f}")
for name, f1, f2 in [
    # (name, f1, f2)
    ("mean", np.mean, np.nanmean),
    ("sum", np.sum, np.nansum),
    ("std", np.std, np.nanstd),
    ("max", np.max, np.nanmax),
    ("min", np.min, np.nanmin)
]:
    r1 = f1(arr)    # f1의 결과
    r2 = f2(arr)    # f2의 결과

    print(f"[{name}] f1: {r1} f2: {r2}")

"""
    [결측치 해결방법]

    1. 전용 함수 사용
        np.nanxxx
    2. 결측치 제거
        arr[~np.isnan(arr)]     (nan이 아닌 값만 추출)
    3. 결측치를 다른 값으로 대체
        arr[np.isnan(arr)] = np.nanmean(arr)    (평균으로 채우기)
"""


