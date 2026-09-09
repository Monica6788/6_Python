"""
    집합 set
"""
# 중복 불가, 순서 없음, 수정 가능
print("=" * 60)

nums = {1, 2, 3, 3, 3, 4, 2}
print(f"nums: {nums}")  # 중복이 허용되지 않으므로 3이 제거되어 나옴

# 비어 있는 상태 표현
empty1 = {}     # 빈 딕셔너리
empty2 = set()  # 빈 셋

print(f"empty1 type: {type(empty1)}")
print(f"empty2 type: {type(empty2)}")
print()

nums = [1, 2, 3, 3, 3, 4, 2]
print(f"원본 데이터: {nums}")
print(f"중복 제거: {set(nums)}")
print(f"중복 제거 리스트: {list(set(nums))}")
print()

# 집합 연산
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(f"합집합 (| 기호 사용) : {a | b}")    # {1, 2, 3, 4, 5, 6}
print(f"교집합 (& 기호 사용) : {a & b}")    # {3, 4}
print(f"차집합 (- 기호 사용) : {a - b}")    # {1, 2}

# 데이터 변경
data = {1, 2}
print(f"data: {data}")

# 추가: add
data.add(3)
print(f"data: {data}")

# 여러 개의 데이터를 추가할 때는 update
data.update([4, 5])
print(f"data: {data}")

data.update([4, 5, 6, 7])   # 중복 데이터는 알아서 거르고 들어감!
print(f"data: {data}")

# 집합에서 "수정"은 의미가 없다. 값을 삭제하고 새로 추가하는 것만 의미가 있음!
# 삭제 discard

data.discard(5)
print(f"data: {data}")

data.discard(99)
print(f"data: {data}")
# 없는 값을 삭제하더라도 오류는 없고 그냥 해당 set에 아무런 변화가 없음!



