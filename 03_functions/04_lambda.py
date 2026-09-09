from functools import reduce    # reduce 함수 사용을 위한 import

"""
    람다식과 고차함수
"""
print("=" * 60)
print(f"{'lambda - 익명 함수':^50}")
print("=" * 60)

def double1(x):
    return x * 2

print(f"일반 함수: {double1(72)}")

# Lambda 표현식 -> lambda 매개변수: 반환식
double2 = lambda x: x * 2

print(f"람다 함수: {double2(72)}")
# 사실 이런 방식보다는 고차함수 안에 람다함수를 많이 사용함!
print()

print("=" * 60)
print(f"{'고차 함수':^52}")
print("=" * 60)
# map(): 전달한 함수를 적용하여 새로운 이터레이터를 반환
print("map(): 전달한 함수를 적용하여 새로운 이터레이터를 반환")

numbers = [n for n in range(1, 11)]
print(f"numbers = {numbers}")
result = list(map(lambda x: x ** 2, numbers))
print(f"map 활용: {result}")
print()

# filter(): 조건을 만족하는 요소만 가지고 새로운 이터레이터 반환
print("filter(): 조건을 만족하는 요소만 가지고 새로운 이터레이터 반환")
result = list(filter(lambda x: x % 2 == 1, numbers))
print(f"filter 활용: {result}")
print()

# sorted(): 데이터를 정렬
print("sorted(): 데이터를 정렬")
print(f"numbers = {numbers}")
print(f"ASC: {sorted(numbers)}")
print(f"DESC: {sorted(numbers, reverse=True)}")
print()

products = [
    {"name": "춘식이 파우치", "price": 3000},
    {"name": "키캡", "price": 300},
    {"name": "브라운 인형", "price": 1000}
]
print(f"products: {products}")
print()

# 가격(price) 기준 DESC
by_price = sorted(products, reverse=True, key=lambda p: p["price"])
# key=lambda p: p["price"] -> key: sorted 함수에게 "정렬 기준이 될 값"을 알려주는 옵션
print("높은 가격순")
for p in by_price:
    print(f"{p['name']}: {p['price']}원")
print()

# 이름(name) 기준 오름차순 정렬
by_name = sorted(products, key= lambda p: p["name"])
print("가나다순")
for p in by_name:
    print(f"{p['name']}: {p['price']}원")
print()

# reduce(): 순회하면서 누적 계산을 수행하는 함수
print("reduce(): 순회하면서 누적 계산을 수행하는 함수")
# import는 사용 직전에 해도 되지만 관례상 코드 가장 윗부분에 작성함
# reduce인데 왜 '누적'이냐? -> 여러 데이터를 하나로 압축시켜 축소(reduce)시킨다고 이해하자!

numbers = [n for n in range(1, 31, 2)]
print(f"{reduce(lambda total, curr: total + curr, numbers, 0)}")
# total: 누적값, curr: 현재값
"""
    초기값 0을 작성하지 않을 경우
    : total 자리에 리스트의 첫 번째 수가 들어가고, curr는 두 번째 수부터 들어감
      => numbers가 빈 리스트일 경우 에러 발생
    
    초기값 0 존재
    : total 자리에 0, curr에 첫 번째 수부터 차례로 들어감
      => numbers가 빈 리스트이더라도 오류 발생 안 함
"""
print()

datas = ["Icecream", "DarkChocolate", "Cake", "Snack"]
# 가장 긴 문자열 찾기
longest = reduce(lambda result, curr: result if len(result) >= len(curr) else curr, datas)
print(f"가장 긴 문자열: {longest}")
print()

# 다양한 내장 함수
numbers = [3, 5, 2, 1, 7, 6]
print(f"numbers = {numbers}")
print(f"길이: {len(numbers)}")
print(f"합계: {sum(numbers)}")
print(f"최댓값: {max(numbers)}")
print(f"최솟값: {min(numbers)}")

print(f"any(n > 5): {any(n > 5 for n in numbers)}")
print(f"all(n > 5): {all(n > 5 for n in numbers)}")