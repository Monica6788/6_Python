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