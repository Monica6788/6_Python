"""
    연산자
"""

print("=" * 60)
print("산술 연산자")
print("=" * 60)

print(f"7 + 3 = {7 + 3}")
print(f"7 - 3 = {7 - 3}")
print(f"7 x 3 = {7 * 3}")
print(f"7 / 3 = {7 / 3}")
print(f"7 / 3 = {7 // 3} ... {7 % 3}")
print(f"7의 3제곱 = {7 ** 3}")

print(f"실수 나눗셈 타입: {type(7 / 3)}")
print(f"실수 나눗셈 타입: {6 / 3} {type(6 / 3)}")   # 나누어 떨어지더라도 결과는 항상 float

print(f"-7 / 3 = {-7 / 3}")
print(f"-7 // 3 = {-7 // 3}")   # 자바에서는 소수점 아래 버림, 파이썬에서는 내림

print("=" * 60)
print("비교, 논리 연산자")
print("=" * 60)

a, b = 2, 5
print(f"a, b --> {a}, {b}")
print(f"a == b --> {a == b}")
print(f"a != b --> {a != b}")
print(f"a < b --> {a < b}")
print(f"a >= b --> {a >= b}")
print()

# 논리 연산자: 자바에서 &&, ||, !로 썼던 연산자들이
#              파이썬에서는 and, or, not
print(f"and --> {True and True}")
print(f"or --> {True or False}")
print(f"or --> {True or True}")
print(f"not --> {not False}")

# a 값이 -5 ~ 5 사이의 값인지 여부
print(f"a가 -5 이상 5 이하: {-5 <= a and a <= 5}")
print(f"a가 -5 이상 5 이하: {-5 <= a <= 5}")

# TODO: 멤버쉽 연산자 (2일차에 계속!)
print("=" * 60)
print("멤버쉽 연산자(in), 식별 연산자(is)")
print("=" * 60)

hunters = ["Dante", "Nero", "Trish"]
print(f"-> {hunters}")
print(f"'Dante' is in hunters: {'Dante' in hunters}")
print(f"'Kyrie' is in hunters: {'Kyrie' in hunters}")
print(f"'Nero' is NOT in hunters: {'Nero' not in hunters}")
print(f"'Leon Scott Kennedy is NOT in hunter: {'Leon Scott Kennedy' not in hunters}")
print(f"{'Cry' in 'DevilMayCry'}\n")

x = [1, 2, 3]
y = [1, 2, 3]
z = x
print(f"x: {x}, y: {y}, z: {z}")

print(f"x, y의 배열 값 동등 비교: {x == y}")     # True
print(f"x, y의 객체 주소 동등 비교: {x is y}")   # False
print(f"x, z의 객체 주소 동등 비교: {x is z}")   # True

# None 비교 시 is 사용을 권장
data = None
print(f"Is 'data' None? -> {data is None}")
print(f"Is NOT 'data' None? -> {data is not None}")

print("=" * 60)
print("복합 대입 연산자")
print("=" * 60)

x = 10
print("x:", x)

# x = x + 5
x += 5
print(f"x += 5 : {x}")

# x = x - 5
x -= 5
print(f"x -= 5 : {x}")

# 파이썬에서는 증감연산자가 존재하지 않음 => (++, -- 사용 불가)
# => 복합 대입 연산자 사용
# 증가 연산자 (++) : 1씩 증가
x += 1
# 감소 연산자 (--) : 1씩 감소
x -= 1

