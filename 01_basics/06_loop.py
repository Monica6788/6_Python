"""
    반복문
"""
print("=" * 60)
print("파이썬의 for문 --> 항상 for-each문")
print("=" * 60)

dmc5 = ["Dante", "Nero", "V"]
for p in dmc5:
    print(p, end="\t")

print()

for c in "DevilMayCry":
    print(c, end=" ")
print()

print("=" * 60)
print("내장 함수 range")
print("=" * 60)

# range(시작, 끝, 간격)
print(f"range(5) -> {list(range(5))}")      # 끝값을 5로 지정. 시작: 0, 간격: 1
print(f"range(1, 6) -> {list(range(1, 6))}")    # 시작값 1, 끝값 6 (6 미만), 간격: 1

# [0, 2, 4, 6, 8] -> 시작: 0 / 간격: 2 / 끝: 9 또는 10
print(f"range(0, 9, 2) -> {list(range(0, 9, 2))}")
print(f"range(0, 10, 2) -> {list(range(0, 10, 2))}")

# [-5, -4, -3, -2, -1] -> 시작: -5 / 간격: 1 / 끝: 0
print(f"range(-5, 0, 1) -> {list(range(-5, 0))} (간격 1은 기본값이므로 생략 가능)")

# [5, 4, 3, 2, 1] -> 시작: 5 / 간격: -1 / 끝: 0
print(f"range(5, 0, -1) -> {list(range(5, 0, -1))}")

# for i in range(11):
#     print(f"2의 {i}제곱 = {2 ** i}")

# print("구구단")
# for i in range(10):
#     for j in range(10):
#         print(f"{i} x {j} = {i * j}")

for i in range(len(dmc5)):
    print(f"[{i}] : {dmc5[i]}")
    # 인덱스처럼 사용!

print("=" * 60)
print("enumerate() - 번호와 값을 함께!")
print("=" * 60)

for i, p in enumerate(dmc5):
    print(f"[{i}] : {p}")

for i, p in enumerate(dmc5, start=1):   # start: 시작번호
    print(f"[{i}] : {p}")

print("=" * 60)
print("zip() - 여러 리스트를 동시에 다루기")
print("=" * 60)

names = ["Leon", "Claire", "Ada"]
mids = [60, 95, 90]
finals = [80, 97, 96]

for name, mid, final in zip(names, mids, finals):
    diff = final - mid
    print(f"{name:<10} : {final:<3}점 (중간고사 점수와 차이: {diff}점)")

print("=" * 60)
print("while문")
print("=" * 60)

count = 0

while count < 5:
    print(f"count 값: {count}")
    count += 1

print()

n = 1
# 반복문 종료 조건: n > 3

while True:
    if n > 3:
        break   # 반복문 종료
    print(f"n : {n}")
    n += 1

print("=" * 60)
print("break / continue / for - else")
print("=" * 60)

print("1 ~ 10 범위에서 홀수만 출력, 단 7을 넘으면 중단")
for n in range(1, 11):
    # 짝수인 경우 다음 루프로 이동
    if n % 2 == 0:
        continue
        """ 
        pass는 쓰면 안 되는 이유
        - continue: 조건이 맞을 때(짝수일 때) 아래 코드를 실행하지 않고
                    즉시 다음 반복(다음 수)으로 건너뜀 
        - pass: "아무것도 하지 않음"이라는 뜻의 placeholder 문법이므로
                짝수일 때도 아래로 코드가 계속 흘러 짝수까지 함께 출력됨
        -             
        """
    # 7보다 큰 경우 반복문 종료 (중단)
    if n > 7:
        break
    else:
        print(n, end=" ")
print()

for p in dmc5:
    if p == "V":
    # if p == "Leon":
        print(f"{p}를 찾았습니다!")
        break
else:
    print("찾는 캐릭터가 없습니다.")