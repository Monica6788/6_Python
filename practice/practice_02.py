import random
# 연습문제
"""
### 1. 몸무게(kg)와 키(cm)를 입력받아 BMI 지수를 계산하는 함수를 정의

- BMI = 몸무게(kg) / (키(m) * 키(m))
- 키는 cm로 입력받아 m로 변환
- 반올림 함수: `round(숫자, 자릿수)`

#### 입출력 예시

```
몸무게를 입력하세요(kg): 70
키를 입력하세요(cm): 175

BMI: 22.86
```
"""
# print("=" * 60)
# print(f"{'1번':^60}")
# print("=" * 60)

# def bmi(height, weight):
#     height_m = height / 100
#     return round(weight / (height_m ** 2), 2)
# weight = float(input("몸무게를 입력하세요(kg): "))
# height = float(input("키를 입력하세요(cm): "))
# print(f"BMI: {bmi(height, weight)}")


"""
### 2. 여러 개의 숫자를 입력받아 평균을 계산하는 함수를 정의

- 사용자가 'q'를 입력할 때까지 숫자를 계속 입력받음 (입력받는 개수는 정해져 있지 않음)
- 평균 = 총합 / 총개수

#### 입출력 예시

```
========== 평균 계산기 ==========
숫자 입력 (q 입력 시 종료) : 1
숫자 입력 (q 입력 시 종료) : 4
숫자 입력 (q 입력 시 종료) : 5
숫자 입력 (q 입력 시 종료) : q

---> 평균: 3.33
```

```
========== 평균 계산기 ==========
숫자 입력 (q 입력 시 종료) : 1
숫자 입력 (q 입력 시 종료) : q

---> 평균: 1.0
```

```
========== 평균 계산기 ==========
숫자 입력 (q 입력 시 종료) : q

---> 값이 없습니다.
```
"""
# print("=" * 60)
# print(f"{'2번':^60}")
# print("=" * 60)

# # 빈 리스트 (입력 받은 수를 담을 공간)
# numbers = []

# # 입력 받은 값이 q이면 반복문 종료, 정수이면 int로 바꾸어 numbers에 추가
# while True:
#     num = input("숫자 입력 (q 입력 시 종료): ")
#     if num == "q":
#         break
#     else:
#         numbers.append(int(num))
# # print(numbers)

# def avg(numbers):
#     # 함수 정의: 합계를 길이(개수)로 나누기 (실수형 나눗셈)
#     # 위 계산의 몫을 소숫점 아래 둘째자리까지 반올림
#     return round(sum(numbers) / len(numbers), 2)

# print(f"평균: {avg(numbers)}")

"""
### 3. 단어 빈도수 분석 함수 정의

- 문장(문자열)을 입력받아 공백 단위로 단어를 분리하고, 각 단어의 등장 횟수를 딕셔너리로 계산하여 반환
- 대소문자를 구분하지 않도록 모든 문자를 소문자로 변환하여 처리
- 소문자 변환: `.lower()`
- 문자열 분리: `.split()`

#### 입출력 예시

```
문장을 입력하세요: Python is fun and Python is powerful

[단어 빈도수 결과]
- python: 2회
- is: 2회
- fun: 1회
- and: 1회
- powerful: 1회
```
"""
print("=" * 60)
print(f"{'3번':^60}")
print("=" * 60)

sentence = input("문장을 입력하세요: ")

# 소문자로 바꾼 후 구분자(공백)로 쪼개어 리스트에 담기
words = sentence.lower().split(" ")
print(words)

# 단어의 빈도수를 담을 딕셔너리 추가 (key: 단어, value: 빈도수)
frequency = {}

def frequency_count(words):
    for word in words:
        frequency[word] = words.count(word)
    return frequency

# 튜플 형태로 키와 밸류를 받아서 튜플의 두 번째 값(빈도수)에 따라 정렬
by_frequency = sorted(frequency_count(words).items(), reverse=True, key = lambda w:w[1])

print("[단어 빈도수 결과]")
for k, v in by_frequency:
    print(f"{k}: {v}회")

"""
### 4. 로또 번호 자동 생성 함수 정의

- 1부터 45 사이의 서로 다른 무작위 숫자 6개를 생성한 후 오름차순으로 정렬하여 반환
- 구매할 게임 수를 입력받아 해당 횟수만큼 로또 번호 세트를 출력
- 정렬: `sorted()`
- 난수: `import random` 후 `random.randint(1, 45)` 활용

#### 입출력 예시

```
구매할 로또 게임 수를 입력하세요: 3

[로또 번호 발급 결과]
1게임: [3, 12, 19, 25, 33, 42]
2게임: [1, 7, 14, 28, 35, 40]
3게임: [5, 11, 21, 22, 38, 45]
```
"""
# print("=" * 60)
# print(f"{'4번':^60}")
# print("=" * 60)

# def lotto_numbers():
#     # 로또 번호를 담을 빈 집합
#     lotto = set()
#     for i in range(1, 7):
#         lotto.add(random.randint(1, 45))
#         i += 1
#     return sorted(list(lotto))

# times = int(input("구매할 로또 게임 수를 입력하세요: "))
# print("[로또번호 발급 결과]")
# for i in range(1, times + 1):
#     print(f"{i}게임: {lotto_numbers()}")
    

"""
### 5. 학생 성적 통계 분석 함수 정의

- 학생들의 이름과 점수가 담긴 딕셔너리를 전달받아 최고 득점자, 최저 득점자, 전체 평균 점수를 계산하여 반환
- 반환값은 `((최고득점자, 점수), (최저득점자, 점수), 평균점수)` 형태로 반환
- 함수 호출 후 반환값을 튜플 언패킹(Unpacking)으로 받아 결과 출력
- **데이터 예시:**
    
    ```python
    {
        "홍길동": 85,
        "이순신": 96,
        "강감찬": 72,
        "유관순": 91
    }
    ```
    

#### 입출력 예시

```
========== 학생 성적 분석 결과 ==========
- 최고 득점자: 이순신 (96점)
- 최저 득점자: 강감찬 (72점)
- 전체 평균: 86.0점
```
"""
# print("=" * 60)
# print(f"{'5번':^60}")
# print("=" * 60)

# 이름과 점수를 담을 딕셔너리
# students = [
#     {"name": "Dante", "score": 55},
#     {"name": "Nero", "score": 75},
#     {"name": "Kyrie", "score": 95},
#     {"name": "Nico", "score": 80}
# ]
# def score_analysis(scores):
#     scores = [student.get("score") for student in students]
#     avg = sum(scores) / len(scores)
#     return max(scores), min(scores), avg

# max, min, avg = score_analysis(students)
# print("========== 학생 성적 분석 결과 ==========")
# print(max, min, avg)

# 데이터 예시 잘못 봐서 다시...

# 이름과 점수를 담을 딕셔너리
# students = {
#     "Dante": 55,
#     "Nero": 75,
#     "Kyrie": 95,
#     "Nico": 80
# }

# scores = students.values()

# def get_max_score(students):
#     max_name = ""
#     for student in students:
#         if students[student] == max(scores):
#             max_name = student
#     return max_name, max(scores)

# def get_min_score(students):
#     min_name = ""
#     for student in students:
#         if students[student] == min(scores):
#             min_name = student
#     return min_name, min(scores)

# def get_avg_score(scores):
#     return round(sum(scores) / len(scores), 1)

# def score_analysis(students, scores):
#     return get_max_score(students), get_min_score(students), get_avg_score(scores)

# (max_name, max_score), (min_name, min_score), avg = score_analysis(students, scores)
# print("========== 학생 성적 분석 결과 ==========")
# print(f"- 최고 득점자: {max_name} ({max_score}점)")
# print(f"- 최저 득점자: {min_name} ({min_score}점)")
# print(f"- 평균: {avg}점")
