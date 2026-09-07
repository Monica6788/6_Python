"""
    변수와 자료형
"""

# 동적 타입 => 타입 선언 생략
name = "Dante"
age = 20
height = 182.4
is_hungry = True    # or False
temp = None         # Java에서 null과 동일
print(name, age, height, is_hungry, temp)

print("=" * 60)
print("기본 자료형 5가지")
print(type(name), type(age), type(height), type(is_hungry), type(temp))
print("=" * 60)

value = 27
print(f"value = {value} : {type(value)}")
value = "스물일곱"
print(f"value = {value} : {type(value)}")
# 이전에 저장한 타입과 이후에 저장한 타입이 달라도 저장 가능
# BUT! 가능한 것과 별개로, 
# 혼란을 방지하기 위해 하나의 변수에는 하나의 타입만 사용하는 것이 권장됨
print("=" * 60)

# 다중 할당
x, y, z = 64, 256, 1024
print(f"x, y, z -> {x}, {y}, {z}")

a = b = c = 6 ** 3
print(f"a = b = c -> {a}, {b}, {c}")

# 값 교환
x, y = y, x
print(f"(x, y) -> ({x}, {y})")

print("=" * 60)

# 타입 힌트
menu: str = "빵이랑 닭가슴살"
print(f"점심 메뉴: {menu} {type(menu)}")

price: int = "6000원"
print(f"가격: {price} {type(price)}")
# 타입 힌트는 강제성이 없으며 에러도 발생되지 않음

print("=" * 60)
# 상수 -> 대문자로 변수명을 작성하는 것을 약속(관례). final 키워드는 없음!

# 최대 인원: 60명 지정
MAX_HEADCOUNT = 60
print(f"최대 인원: {MAX_HEADCOUNT}명")
# 이름만 상수지 값을 변경할 수 있으므로 내가 만든 상수가 아닌 이상 값을 바꾸지 말자!