"""
    함수 (function)
    - 정의에 사용하는 키워드: def
"""
print("=" * 60)
print(f"{'함수':^56}")
print("=" * 60)

# 함수 정의
def hello(name):
    return f"{name}님 안녕하세요."

# 함수 호출
print(hello("Monica"))
result = hello("Dante")
print(result)
# hello 함수: 매개변수(name) O, 반환값(f"{name}님 안녕하세요.") O

def hello_print(name):
    print(f"{name}님 반갑습니다.")
    # return 생략됨

hello_print("Nero")
print(hello_print("Kyrie"))     # 반환값이 없는 함수의 반환값을 출력했으므로 None
result = hello_print("Kyrie")
print(f"result: {result}")      # 이 역시 None
print()

# 여러 값을 반환하는 함수
def calc(a, b):
    return a + b, a - b, (a + b) * (a - b)

result = calc(30, 1)
print(f"result: {result}")

# 언패킹
add, sub, diff_of_squares = calc(20, 1)
print(f"result: {add} / {sub} / {diff_of_squares}")

print("=" * 60)
print(f"{'docstring (함수 설명)':^54}")
print("=" * 60)

def calc_vat(price, rate=0.1):    # rate 기본값 0.1
    """
    부가세를 포함한 최종 가격을 반환하는 함수
    Args:
        price: 부가세 제외 금액
        rate: 부가세율 (기본 10%)
    Returns:
        부가세 포함 금액
    """
    return int(price * (1 + rate))

print(f"5000원 ---> {calc_vat(5000):,}원")  # :,는 천 단위마다 콤마를 찍어주는 포맷 지정자
help(calc_vat)

# 주의! 파이썬은 호이스팅 개념이 없으므로 함수 정의 전에 호출 불가!
# print(test())       # NameError: 'test'라는 함수가 정의되어 있지 않음!

def test():
    return "테스트 함수"

