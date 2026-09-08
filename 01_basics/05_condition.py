"""
    조건문
"""
print("=" * 60)
print("if / elif / else")
print("=" * 60)

value = 10

if value > 5:
    print("조건문 내부")
    print("조건문 내에서 실행하려면 들여쓰기 필수!!!")

print("조건문 외부")

score = 100    # int(input("Enter your score: "))
if score == 100:
    grade = "Smokin' Sexy Style!"
elif score >= 95:
    grade = "Sick Skills"
elif score >= 90:
    grade = "Savage"
elif score >= 80:
    grade = "Apocalyptic"
else:
    grade = "Badass"

print(f"{score}점 => {grade}")
# 블록은 들여쓰기로 구분, 조건식 옆에는 콜론(:) 지정
# else if 대신 elif 사용

print("=" * 60)
print("삼항 연산")
print("=" * 60)

# 참일때결과값 if 조건식 else 거짓일때결과값
age = 64 # int(input("나이 입력: "))
"""
if age >= 20:
    result = "Adult"
else:
    result = "Minor"
"""

result = "Adult" if age >= 20 else "Minor"

print(f"{age} years old -> {result}")

print("=" * 60)
print("match-case (java의 switch)")
print("=" * 60)

status = 200 # int(input("상태 코드 입력: "))
"""
switch (status) {
    case 200:
        result = "정상"
        break;
    case 404:
        result = "페이지를 찾을 수 없음"
        break;
    case 500:
        result = "서버 오류"
        break;
    default:
        result = "알 수 없는 오류"
        break;
}
"""

match status:
    case 200:
        result = "정상"
        # 파이썬에서는 들여쓰기로 블록 구분! => break 안 써도 됨!
    case 404:
        result = "페이지를 찾을 수 없음"
    case 500:
        result = "서버 오류"
    case _:
        result = "알 수 없는 오류"

print(f"{status} -> {result}")

print("=" * 60)
print("pass: 미구현 블록의 placeholder")
print("=" * 60)

# 빈 블록을 작성하고자 할 때 사용
# (빈 블록만 덩그러니 두면 오류 발생 => 오류 방지용)
score = 81
if score > 80:
    pass    # 미구현 부분을 임시로 처리
else:
    print("조금 더 노력합시다!")

