"""
    브로드 캐스팅
    
    - 형태(모양, 즉 shape)가 서로 다른 배열끼리 연산을 수행할 때
      작은 배열이 자동으로 확장하여 크기를 맞춰주는 기능
"""
import numpy as np
from load_utils import load_matrix

a = np.arange(1, 7).reshape(2, 3)
print(f"a + 10\n{a + 10}")
"""
    10이라는 값 하나가 배열 전체에 적용됨.
    numpy가 10을 () -> (2, 3) 크기로 늘려서 계산이 되는 것처럼 동작 (브로드 캐스팅)
"""

"""
    1. 뒤에서부터 차원 비교
    2. 크기가 같거나, 둘 중 하나가 1이면 통과
    3. 차원 수가 다르면 앞쪽에 1을 채워 맞춰준다

    ex. (120, 750) + (750,) --> (120, 750) + (1, 750)
"""
cases = [
    ((120, 750),  None, "None"),
    ((120, 750), (750,), "(750,)"),
    ((120, 750), (120, 1), "(120, 1)"),
    ((120, 750), (1, 750), "(1, 750)"),
    ((120, 750), (120,), "(120,)"),
    ((120, 750), (100,), "(100,)")
]

for a_shape, b_shape, label in cases:
    arr_a = np.ones(a_shape)
    arr_b = 2.0 if b_shape is None else np.ones(b_shape)

    try:
        result = (arr_a + arr_b).shape
    except ValueError:
        result = "ValueError"

    print(f"{a_shape} + {b_shape} : {result}")

"""
    오류 발생
        (120, 750) + (120, ) => 750 vs 120이 되어 오류 발생
                                (크기도 다르고 둘 다 1이 아님)
        (120, 750) + (100, ) => (100,) 앞에 1이 채워져 (1, 100)이 됨
                             => 750 vs 100이 되어 오류 발생
"""
matrix = load_matrix()
# (120, 750)
# 종목별 평균
means_w = matrix.mean(axis=1)       # (120, )

# print(f"{matrix - means_w}")      # 브로드캐스팅 오류 발생
# ValueError: operands could not be broadcast together with shapes (120,750) (120,)
# means_w를 계산하면 axis=1이라서 열 축이 사라지기 때문.
# => keepdims=True 사용
means = matrix.mean(axis=1, keepdims=True)  # (120, 1)
print(f"{(matrix - means).shape}")          # (120, 750)

