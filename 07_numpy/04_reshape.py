"""
    reshape(shape정보) : 배열을 재구성

    * 배열 요소의 총 개수는 유지되어야 함
        (12, ) --> (1, 12) / (12, 1) / (3, 4) / (2, 6) / ...

    * 한 축의 크기를 자동으로 계산하고자 할 경우, -1 지정
        (단! -1은 딱 1번만 사용 가능)
"""
import numpy as np

# TODO 0~11까지 데이터를 포함하는 1차원 배열 생성
print(f"{'=' * 29} {'reshape'} {'=' * 29}")

arr = np.arange(12)
print(f"{arr}\nshape: {arr.shape}")
print()

# 1차원 배열(12,)을 2차원 배열(3, 4)로 구성
arr_2d = arr.reshape(3, 4)
print(f"(12,) ---> (3, 4)")
print(f"{arr_2d}\nshape: {arr_2d.shape}")
print()

arr_2d_2 = arr.reshape(2, 6)
print(f"(12,) ---> (2, 6)")
print(f"{arr_2d_2}\nshape: {arr_2d_2.shape}")
print()

# -1 지정
arr_2d_3 = arr.reshape(4, -1)
print(f"(12,) ---> (4, -1)")
print(f"{arr_2d_3}\nshape: {arr_2d_3.shape}")
print()

arr_2d_4 = arr.reshape(-1, 6)
print(f"(12,) ---> (-1, 6)")
print(f"{arr_2d_4}\nshape: {arr_2d_4.shape}")
print()

# arr.reshape(-1, -1)
# ValueError: can only specify one unknown dimension

print(f"{'=' * 29} {'3차원 배열로 reshape'} {'=' * 29}")
arr_3d = arr.reshape(2, 2, 3)
print(f"(12,) ---> (2, 2, 3)")
print(f"{arr_3d}\nshape: {arr_3d.shape}")
print()

arr_3d_1 = arr.reshape(3, 2, -1)
print(f"{arr_3d_1}\nshape: {arr_3d_1.shape}")
print()

# arr.reshape(2, -1, -1)
# ValueError: can only specify one unknown dimension
# 차원 수가 커져도 -1은 한 번만 사용 가능

print(f"{'=' * 26} {'다차원 -> 1차원 reshape'} {'=' * 26}")
arr_1d_f = arr_3d.flatten()
print(f"flatten: {arr_1d_f} / {arr_1d_f.base is arr_3d}")     # 복사본 (독립된 메모리)
print(f"arr_1d_f의 base: {arr_1d_f.base}")
print()

arr_1d_r = arr_3d.ravel()
print(f"ravel : {arr_1d_r} / {arr_1d_r.base is arr_3d}")      # 뷰 (원본과 메모리 공유)
print(f"arr_1d_r의 base: {arr_1d_r.base}")
print()
# ravel이 복사본을 반환하는 경우
#   메모리가 연속적으로 배치된 경우에만 뷰를 반환
#   메모리가 불연속적인 경우 (ex. 전치행렬, .T 등) 복사본을 반환
#   .base 속성으로 뷰인지 복사본인지 확인 가능
#       => arr_1d_2.base is arr_3d : True이면 뷰, False이면 복사본

# reshape(-1)을 하면 1차원 배열로 바꾸어줌
# reshape는 기본적으로 뷰를 반환하므로 아래 둘 다 뷰
arr_1d_3 = arr_3d.reshape(-1)
print(f"reshape(-1) : {arr_1d_3} / {arr_1d_3.base is arr_3d}")
print(f"arr_1d_3의 base: {arr_1d_3.base}")
print()

arr_1d_2 = arr_2d.reshape(-1)
print(f"reshape(-1) : {arr_1d_2} / {arr_1d_2.base is arr_2d}")
print(f"arr_1d_2의 base: {arr_1d_2.base}")
print()

"""
    flatten: [ 0  1  2  3  4  5  6  7  8  9 10 11] / False
    arr_1d_f의 base: None

    ravel : [ 0  1  2  3  4  5  6  7  8  9 10 11] / False
    arr_1d_r의 base: [ 0  1  2  3  4  5  6  7  8  9 10 11]
        

    reshape(-1) : [ 0  1  2  3  4  5  6  7  8  9 10 11] / False
    arr_1d_3의 base: [ 0  1  2  3  4  5  6  7  8  9 10 11]

    reshape(-1) : [ 0  1  2  3  4  5  6  7  8  9 10 11] / False
    arr_1d_2의 base: [ 0  1  2  3  4  5  6  7  8  9 10 11]

    * 왜 View를 반환하는 것들까지 .base가 False인가?
      => arr_2d, arr_3d는 모두 원본 배열인 arr의 View였기 때문!
      arr = np.arange(12)
"""
