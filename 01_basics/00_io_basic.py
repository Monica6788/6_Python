"""
    출력 함수
    - print()
"""
print("=" * 75)     # "="를 75번 반복하여 출력 (곱하기)
print("기본 출력 확인")
print("=" * 75)

# 문자열은 따옴표("", '')로 감싸서 표현
print("hello, python!")
print('nice to meet you, python!')

# 슷자는 따옴표 없이 값 그래도 표현
print(1024)
print(2.71)
print(3 ** 5)

# 여러 값을 한 번에 출력. 콤마(,)로 구분
print("Dante", 20, "Red")

# 구분자를 지정하여 출력: sep 옵션 사용 (기본값: 공백)
print("2026", "09", "07", "MON", sep=".")

# 마지막 출력 문자 지정: end 옵션 사용 (기본값: 개행 = \n)
print("첫 번째 줄",  end=" ")
print("두 번째 줄")
"""
print("첫 번째 줄")
print("두 번째 줄")
위와 같이 작성 시 한 줄씩 나오는데, end=" "를 지정하면 '첫 번째 줄 두 번째 줄'과 같이 한 줄에 나옴
"""
print("=" * 75)
print("이스케이프 문자")
print("=" * 75)

# \로 이스케이프 문자 사용
print("이번 줄 다음에 출력하겠습니다.\n한 줄 개행")
print("탭 간격을 주겠습니다.\t한 탭 처리")
print("속마음: \"배고프다\"")   # 큰따옴표를 문자 그 자체로 쓰기 위해 \를 사용함

print("=" * 75)
print("문자 형식 지정 (포매팅)")
print("=" * 75)

name = "Nero"
age = 22
height = 182.5

# Java의 printf와 유사
print("이름: %s, 나이: %d세, 키: %.2fcm" %(name, age, height))

# 문자열.format() 메서드 사용
print("이름: {}, 나이: {}세, 키: {}cm".format(name, age, height))

# f-string :  문자열 표현 방법(형식 지정)
print(f"이름: {name}, 나이: {age}세, 키: {height}cm")
print(f"내년에는 {age + 1}살이 됩니다.")   # 계산이 가능하다.

# 정렬 기능 ({변수:옵션})
print(f"[{name:<10}]")  # <10 : 10칸 확보, 왼쪽 정렬
print(f"[{name:>10}]")  # >10 : 10칸 확보, 오른쪽 정렬
print(f"[{name:^10}]")  # ^10 : 10칸 확보, 가운데 정렬

"""
    입력 함수
    - input()
"""
print("=" * 75)
print("입력 받아보기")
print("=" * 75)

age_str = input("나이(문자열) 입력: ")
print(f"입력값: {age_str}, 타입: {type(age_str)}")  # str로 나옴
# 입력값은 항상 문자열로 처리된다
# => 계산이 필요한 경우 형변환이 필요하다

age = int(input("나이 입력: "))
print(f"내년에는 {age + 1}살이 됩니다. {type(age)}")