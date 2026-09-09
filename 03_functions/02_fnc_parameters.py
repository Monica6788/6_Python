"""
    매개변수 (parameter)
"""
print("=" * 60)
print(f"{'기본값 매개변수':^50}")
print("=" * 60)

# 전달된 값이 없을 경우 기본값으로 저장해서 사용
def connect(host, port=8080, charset='utf-8'):
    print(f"전달된 정보: {host}:{port} ({charset})")

connect("localhost")
connect("localhost", 1521)
connect("localhost", 1521, "euc-kr")
# 기본값을 갖는 매개변수는 뒤쪽에 배치!
print()

print("=" * 60)
print(f"{'키워드 매개변수':^50}")
print("=" * 60)

connect(port=1521, charset="utf-10", host="localhost")
# 키워드를 지정하면 순서와 상관없이 값을 전달할 수 있음
print()

print("=" * 60)
print(f"{'가변 매개변수: *변수명':^50}")
print("=" * 60)

# 개수가 정해지지 않은 값들을 전달 받을 때 사용
def total(*numbers):
    print(f"전달 받은 값: {numbers} {type(numbers)}")   # 튜플 형태
    return sum(numbers)
print(f"total(1, 3) -> {total(1, 3)}")
print(f"total(1, 3, 5, 7) -> {total(1, 3, 5, 7)}")
print(f"total() -> {total()}")
print()

print("=" * 60)
print(f"{'키워드 가변 매개변수: **변수명':^50}")
print("=" * 60)

# 특정 키워드를 지정하여 값들을 전달 받을 때 사용
def create_user(**data):
    print(f"전달 받은 값: {data} {type(data)}")     # 딕셔너리 형태
    for k, v in data.items():
        print(f"{k} : {v}")

create_user(name="Monica", age=20, address="Korea")
print()

def log(level, *message, **options):
# 매개변수 작성 순서 def log(level, temp=200, *message, **options):
# 주의! 가변인자, 키워드 가변인자는 함수 1개당 하나씩만 사용 가능
    print(f"level: {level}")
    print(f"messages: {message}")
    print(f"options: {options}")

log("INFO", "서버 시작", "포트번호 8080...", color="green", timestamp=True)
