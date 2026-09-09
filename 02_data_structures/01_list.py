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

# 탐색 및 정보 조회
numbers = [5, 1, 2, 7, 9, 4, 1]

# 찾을값 in 리스트명 => 값이 있으면 True, 없으면 False
# 리스트명.index(찾을값) => 값이 있으면 해당 값의 인덱스 반환, 없으면 ValueError 발생

print(f"Is there 7 in numbers? -> {7 in numbers}")
print(f"What is the index of 7 in numbers? -> {numbers.index(7)}")

print(f"Is there 7 in numbers? -> {17 in numbers}")
# print(f"What is the index of 7 in numbers? -> {numbers.index(17)}")   # ValueError 발생!

print(f"Count of 1 in numbers -> {numbers.count(1)}")
print(f"Count of 3 in numbers -> {numbers.count(3)}")

print(f"Length of numbers list -> {len(numbers)}")

print(f"{numbers}")
numbers.sort()      # 해당 리스트의 값을 변경한 것!
print(f"After sort() -> {numbers}")     # asc
numbers.sort(reverse=True)
print(f"After sort(reverse=True) -> {numbers}")     # desc

games = ["Devil May Cry", "Hades", "StardewValley"]
games.sort()
print(f"Sorting str -> {games}")
games.reverse()                 # 해당 리스트를 역순으로 변경
# 오름차순/내림차순 아니고 원래 순서에서 뒤집기만 한 것!
print(f"After reverse() -> {games}")

print("=" * 60)
print("2차원 리스트")
print("=" * 60)

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[::2][::2])
# 1, 3, 7, 9가 선택되는 것이 아니라 [[1, 2, 3]]이 선택됨
# print(maxrix[::2])의 값이 [[1, 2, 3], [7, 8, 9]]
# => 그 안에서 다시 시작 0, 끝 0 간격 2로 고른 것
print()

# 1, 3, 7, 9를 고르려면?
for i in range(0, 3, 2):
    for j in range(0, 3, 2):
        print(matrix[i][j], end=" ")
print()

print(f"1행 1열 -> {matrix[1][1]}")
print()

for row in matrix:
    # print row
    for value in row:
        print(value, end=" ")
    print()


