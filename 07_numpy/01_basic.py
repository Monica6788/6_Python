"""
    Numpy (넘파이)

    다차원 배열을 다룰 수 있는 기능을 제공하는 라이브러리
    넘파이 배열: ndarray
"""
import numpy as np

# 파이썬 리스트에는 다양한 타입의 데이터를 담을 수 있음
print(f"========== 파이썬 리스트 복습 ==========")
data_list = [1, "이", 3.0, [4]]
print(f"data_list : {data_list}")
# __name__ 속성으로 이름만 쏙 빼오기 (<class 'int'>에서 int만 나오도록)
print(f"각 요소별 타입: {[type(x).__name__ for x in data_list]}")

data_list2 = [10, 20, 30, 40]
print()

"""
print("-" * 60)
for d1, d2 in zip(data_list, data_list2):
    print(f"{d1} + {d2} = {d1 + d2}")
    # TypeError: can only concatenate str (not "int") to str 발생
print("-" * 60)
"""
# 파이썬의 리스트는 데이터를 구분하지 않고 담을 수 있는 점이 편리할 수 있지만,
#   다른 리스트와 연사을 하고자 할 때는 문제가 될 수 있음.

# 넘파이 배열 (ndarray)는 데이터 타입이 하나로 고정된 구조로, 연산이 쉽다.
print(f"========== 넘파이 배열 ndarray ==========")
arr  = np.array([1, 2, 3, 4])
print(f"arr : {arr}")
print(f"배열 타입 : {arr.dtype}")
print()

arr2 = np.array([8, 7, 6, 5])
print(f"arr2 : {arr2}")
print()

for d1, d2 in zip(arr, arr2):
    print(f"{d1} + {d2} = {d1 + d2}")

print(f"arr + arr2 = {arr + arr2}")
# 넘파이 배열은 자바의 배열과 비슷하지만,
#   연산 수행 시 반복문을 사용하지 않고, 배열 단위의 연산이 가능 (벡터화 연산)
print()
print("-" * 60)

# 넘파이 배열의 차원과 형태
print()
print(f"========== 넘파이 배열의 차원과 형태 ==========")
# 0차원 배열 -> 스칼라 (단일 값)
arr_0d = np.array(42)
print(f"0차원 배열: {arr_0d} / 차원: {arr_0d.ndim} / 형태: {arr_0d.shape}")
# 0차원 배열: 42 / 차원: 0 / 형태: ()

# 1차원 -> 벡터 (0차원의 모임)
arr_1d = np.array([1, 2, 3])
print(f"1차원 배열: {arr_1d} / 차원: {arr_1d.ndim} / 형태: {arr_1d.shape}")
# 1차원 배열: [1 2 3] / 차원: 1 / 형태: (3,)

# 2차원 -> 행렬 (1차원의 모임)
arr_2d = np.array([[1, 2, 3], [4, 5, 6]])
print(f"2차원 배열: \n{arr_2d}\n / 차원: {arr_2d.ndim} / 형태: {arr_2d.shape}")
# 2차원 배열: 
# [[1 2 3]
#  [4 5 6]]
#  / 차원: 2 / 형태: (2, 3)
print()
print("-" * 60)

n = 100_000         # 숫자 표현 시 _로 구분 가능 (세 자리마다 콤마 찍듯이)
print(f"n: {n}")

# 리스트와 배열을 0 ~ 99_999 데이터로 생성
list_100k = list(range(n))
arr_100k = np.arange(n)

print(f"list_100k : {list_100k[:5]} ... {list_100k[-5:]}")
print(f"arr_100k : {arr_100k[:5]} ... {arr_100k[-5:]}")

# 할당된 메모리 크기 비교
import sys

list_container = sys.getsizeof(list_100k)
int_obj = sys.getsizeof(list_100k[0])
list_bytes = list_container + (int_obj * n)

arr_bytes = arr_100k.nbytes

print(f"데이터 {n:,}개 기준")
print(f"- 리스트 : {list_bytes / 1024 / 1024:6.2f} MB")     # 3.43 MB
print(f"- 배열: {arr_bytes / 1024 / 1024:6.2f} MB")          # 0.76 MB

# 10만 개 기준으로 약 2~3MB 정도 차이

