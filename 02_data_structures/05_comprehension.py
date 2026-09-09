"""
    컴프리헨션 (Comprehension)
    => 간결하고 직관적인 데이터 구조 생성 문법 (리스트, 딕셔너리, 셋)
"""
print("=" * 60)
print(f"{'리스트 컴프리헨션':^50}")
print("=" * 60)

nums = []
print(f"nums: {nums}")
for n in range(1, 21):
    nums.append(n)

print(f"nums = {nums}")

# 리스트 컴프리헨션: [표현식 for 변수 in 반복대상]
nums = [n for n in range(1, 21)]
print(f"nums (컴프리헨션) : {nums}")

nums = [n ** 2 for n in range(1, 21)]
print(f"nums (컴프리헨션): {nums}")
print()

# 조건에 해당하는 데이터만 포함할 때: [표현식 for 변수 in 반복대상 if 조건]
nums = [n for n in range(1, 21)]
print(f"Only even nums: {[n for n in nums if n % 2 == 0]}")
print(f"Only mutiples of 3: {[n for n in nums if n % 3 == 0]}")
print()

print("=" * 60)
print(f"{'딕셔너리 컴프리헨션':^50}")
print("=" * 60)
# 딕셔너리 컴프리헨션: {키_표현식:밸류_표현식 for 변수 in 반복대상 if 조건}
menus = ["카레", "베이글", "계란새우스크램블", "더블쿼터파운더치즈버거"]

# 키 -> 메뉴명, 밸류 -> 메뉴명의 길이
menus_dict = {m:len(m) for m in menus}
print(f"menus_dict: {menus_dict}")

menus_dict = {m:len(m) for m in menus if len(m) > 5}
print(f"menus_dict: {menus_dict}")
print()

print("=" * 60)
print(f"{'셋 컴프리헨션':^50}")
print("=" * 60)
# 셋(set) 컴프리헨션: {표현식 for 변수 in 반복대상[ if 조건]}
message = "Smokin' Sexy Style!"

# 문자열에서 고유한 문자만 추출 (중복된 문자 제외)
unique_char = {ch for ch in message}
print(f"'{message}'의 고유 문자: {unique_char}")

# 문자열에서 고유한 문자만 추출 (중복된 문자 제외, 불필요한 부분 제외)
unique_char = {ch for ch in message if ch != "\'" and ch != " " and ch != "!"}
print(f"'{message}'의 고유 문자: {unique_char} / ({len(unique_char)})")


