"""
    딕셔너리 (dict)
"""
# JSON 형식과 유사 (key-value 형태)
# key-value 형태로 데이터를 관리
print("=" * 60)
user = {
    "name": "Monica",
    "age": 20,
    "skills": ["Java", "SQL", "html/css", "JavaScript", "Python"],
}

print(f"user: {user}")
# 딕셔너리 내의 데이터 접근 -> 키값 사용
print("직접 접근")
print(f"이름: {user['name']}")
print(f"스킬: {user['skills']}")
# print(f"연락처: {user['phone']}")
# KeyError: 직접 접근 시에 존재하지 않는 키값은 오류 발생!
print()

print("get() 메서드로 접근")
print(f"이름: {user.get('name', 'NoName')}")
print(f"스킬: {user.get('skills', 'Empty List')}")
print(f"연락처: {user.get('phone')}")       # 존재하지 않는 키값인 경우 None 반환
print(f"이메일: {user.get('email', 'example@email.com')}")  # 기본값 지정 가능
print()

# 변경 (추가/수정/삭제)
user['email'] = 'monica6788@email.com'  # 새로운 키값을 지정 시 추가
print(f"{user}")    # 기존에 존재하지 않던 키값으로 입력 시 추가

user['age'] = 24    # 존재하던 키값을 지정 시 값 수정
print(f"{user}")

del user['age']
print(f"{user}")

"""
del user['phone']   # KeyError: 존재하지 않는 키값으로 삭제하려고 할 경우 오류 발생!
print(f"{user}")
"""
print()

# 탐색
for key in user:
    print(f"key: {key} / value: {user[key]}")

# items() 메서드 사용 시 튜플 형태로 반복문 사용 가능
for k, v in user.items():   # k, v가 튜플
    print(f"key: {k}, value: {v}")
print()

# key값 순회 시 keys() 메서드, value 값 순회 시 values() 메서드 사용
print(f"키 목록: {list(user.keys())}")
print(f"밸류 목록: {list(user.values())}")
# items() 메서드로 (key, value) 튜플 형태 조회 가능
print(f"items(): {list(user.items())}")


