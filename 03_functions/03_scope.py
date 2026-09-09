"""
    스코프 (scope)

    - 전역 변수 (Global Variable)
      : 함수 외부에 선언된 변수
    
    - 지역 변수 (Local Variable)
      : 함수 내부에 선언된 변수. 해당 함수 내에서만 접근 가능
"""
print("=" * 60)
print(f"{'지역변수':^56}")
print("=" * 60)
print("함수 안에서 만든 변수는 함수 밖에서 볼 수 없다.")

count = 0          # 전역 변수

def increase1():
    count = 10      # 지역 변수
    print(f"count (local): {count}")

increase1()                         # 10
print(f"count (global): {count}")   # 0

def increase2():
    # count += 1
    # 전역변수를 사용하려먼 global 키워드 사용
    global count    # global: 전역변수 사용 명시
    count += 1

# increase2()
# print(f"count: {count}")    # UnboundLocalError: 지역변수 'count'가 할당되지 않았다

increase2()
increase2()
print(f"count: {count}")
print("스코프 검색 순서: Local -> Enclosing -> Global (-> Built-in)")
print()

data = "--- Global ---"

def outer():
    data = '--- 바깥 함수 (outer)'

    def inner():
        data = '--- 안쪽 함수 (inner) ---'
        print(f"inner :: data - {data}")

    inner()
    print(f"outer :: data - {data}")

outer()
print(f"전역에서 확인 :: data - {data}")




