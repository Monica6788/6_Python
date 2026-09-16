"""
    넘파이 배열 - 검색, 정렬

    - where: 조건에 맞는 요소의 인덱스 반환 / 값 치환
    - argmax / argmin: 최댓값/최솟값이 있는 인덱스를 반환
    - sort: 정렬
"""
import numpy as np

arr = np.array([10, 5, 22, 15, 8, 20])
print(f"arr : {arr}")

# 15보다 큰 값 찾기
# np.where(조건): 조건에 해당하는 인덱스들을 반환
idx_info = np.where(arr > 15)
print(f"idx_info: {idx_info}")
# 조건에 맞는 값들인지 해당 인덱스를 통해 확인
print(arr[idx_info])

# 10보다 큰 값은 99로 변경, 아닌 값은 0으로 변경
# np.where(조건, 조건을만족하면_변경할값, 조건을만족하지않으면_변경할값)
#    => 조건에 따라 변경된 값으로 구성된 배열 반환
arr2 = np.where(arr > 10, 99, 0)
print(f"arr2 : {arr2}")
print()

arr = np.array([[10, 20, 5], [33, 15, 40]])
print(arr)

# argmax: 최댓값의 인덱스 반환
# argmin: 최솟값의 인덱스 반환
print(f"argmax: {np.argmax(arr)}")      # 5
print(f"argmin: {np.argmin(arr)}")      # 2

print(arr.flatten())
# argmax / argmin은 2차원 배열을 1차원으로 변환했을 때를 기준으로 인덱스를 반환해줌
print()

# 축 (axis) 기준으로 조회
#   axis=0: 열을 기준으로 조회 => y축
#   axis=1: 행을 기준으로 조회 => x축
print(f"열 기준 최댓값 인덱스: {np.argmax(arr, axis=0)}")
print(f"행 기준 최댓값 인덱스: {np.argmax(arr, axis=1)}")
print()

arr = arr.flatten()
print(f"arr: {arr}")
# np.sort(배열): 원본 배열을 변경하지 않고, 정렬된 새로운 배열을 반환
sorted_arr = np.sort(arr)
print(f"np.sort(arr)로 정렬된 배열: {sorted_arr}")     # ASC

desc_arr = sorted_arr[::-1]         # DESC: 오름차순 정렬 후 역순으로 배치하면 됨
print(desc_arr)

# 배열.sort() : 원본 배열 자체를 정렬시켜줌
print(f"arr : {arr}")
arr.sort()
print(f"arr.sort()로 정렬된 배열: {arr}")