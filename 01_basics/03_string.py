"""
    문자열 다루기
"""

print("=" * 60)
print("인덱싱, 슬라이싱")
print("=" * 60)

# 인덱스틑 0부터 시작 (양수 인덱스 기준)
message = "Let's Rock! Sweet Dreams..."
print(f"메시지: {message}")
print()
# 인덱싱: 변수[인덱스]
print(f"첫 글자: {message[0]}")
print(f"마지막 글자: {message[-1]}")

# 슬라이싱: 변수[시작:끝:간격]
print(f"{message[0:11:1]} / {message[0:11]} / {message[:11]}")
print(f"{message[12:]}")
print(f"{message[::2]}")    # 2칸 간격
print(f"{message[::-1]}")   # -1. 역순

print("=" * 60)
print("다양한 문자열 메서드")
print("=" * 60)

# 대문자 변환 : 문자열.upper()
print(f"대문자 변환: {message.upper()}")
# 소문자 변환 : 문자열.lower()
print(f"소문자 변환: {message.lower()}")

message = "   I'm the one with the power   "
print(f"[{message}]")
# 좌우 공백 제거 : strip()
print(f"좌우 공백 제거: [{message.strip()}]")

# 문자열을 구분자로 분할: split(구분자)
message = "Let's Rock! Sweet Dreams..."
print(f"split: [{message.split('! ')}]")

# 특정 문자 개수 반환: count(문자)
print(f"l의 개수(알파벳 소문자 L): {message.count('l')}")
print(f".의 개수(dot): {message.count('.')}")

# 특정 문자의 인덱스 반환: find(문자) or find(문자열)
print(f"Rock의 위치: {message.find('Rock')}")
print(f"Deadweight의 위치: {message.find('Deadweight')}")   # 없으면 -1 반환

# 리스트 --> 문자열 (문자열 결합)
today = '-'.join(["2026", "09", "07", "MONDAY"])
print(today)
print(f"today: {today} {type(today)}")

print("=" * 60)
print("여러 줄 문자열")
print("=" * 60)
# 여러 줄 문자열 => 따옴표 3개
end_message = """
    문자열 다루기
    - 인덱싱, 슬라이싱
    - 자주 사용하는 메서드: split, join, strip, ...
"""

print(end_message)