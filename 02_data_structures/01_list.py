"""
    리스트 (list)
"""
# 리스트 데이터 표현: 대괄호 [] 사용
animes = ["Delicious in Dungeon", "SPY X FAMILY", "Mob Psycho"]
print(f"animes -> {animes}")

# 첫 번째 요소 출력
print(f"1st: {animes[0]}")
# 마지막 요소 출력
print(f"last: {animes[-1]}")
# 슬라이싱 (1, 2번째 요소)
print(f"{animes[0:2]}")

# 다양한 타입의 데이터를 담을 수 있음
mixed = [1024, "제곱수 좋아", True, [2, 3, 5, 7, "소수도 좋아"]]
print(f"mixed: {mixed}")
print(f"{mixed[3][4]}")

# 리스트의 상태에 따라 bool 타입 확인
temp = []
print(f"mixed --> {bool(mixed)}")
print(f"temp --> {bool(temp)}")

print("=" * 60)
snacks = ['오징어땅콩', '포카칩', '참크래커']
print(f"original snacks -> {snacks}")

# 데이터 추가: append(), insert(), extend()
snacks.append("눈을감자")
print(f"append 후 snacks -> {snacks}")

snacks.insert(1, "초코칩쿠키")
print(f"insert 후 snacks -> {snacks}")

snacks.extend(["고래밥", "뿌셔뿌셔"])
print(f"extend 후 snacks -> {snacks}")

# 수정 / 삭제
print("=" * 60)
snacks[0] = "캬라멜땅콩"
print(f"특정 인덱스를 지정하여 값을 변경: {snacks}")

snacks.remove("눈을감자")
print(f"remove - 값으로 삭제: {snacks}")
# snacks.remove("미쯔")     # 해당 데이터가 없을 경우 ValueError 발생!

snacks_pop = snacks.pop()
print(f"pop -  맨 뒤의 데이터 삭제 후 반환: {snacks_pop} / {snacks}")

del snacks[1]
print(f"del - 인덱스로 삭제: {snacks}")