"""
    튜플 (tuple)
"""
# 튜플을 생성하는 방법 -> ()
point1 = (10, 20)
point2 = 50, 60

single1 = (10,)     # 데이터가 1개일 때 콤마 필수!
single2 = (10)      # 왼쪽처럼 작성할 시 튜플이 아닌 int로 인식됨

print(f"point1: {point1} {type(point1)}")
print(f"point2: {point2} {type(point2)}")
print(f"single1: {single1} {type(single1)}")
print(f"single2: {single2} {type(single2)}")
print()

print(f"point1[0]: {point1[0]}")      # 인덱스 접근은 가능
# point1[9] = 99                      # TypeError 발생! 수정 불가 (불변성)
print()

point1 = (99, 20)
print(f"point1 자체를 변경: {point1}")
# 객체가 참조하는 값을 바꾸는 것은 가능!
# 즉, 새로운 튜플 할당은 가능. 튜플 안에 들어 있는 값을 변경할 수 없는 것임!
print()

# 언패킹
x, y = (2, 6)
print(f"x, y : {x}, {y}")

def get_numbers():
    return 77, 44

x, y = get_numbers()
print(f"x, y: {x}, {y}")
print()

# 튜플 내에서 불필요한 값을 무시 => _(언더바, 언더스코어) 사용
# x, y, z = (10, 20, 30)
x, _, z = (10, 20, 30)
print(f"{x}, {z}")
# print(f"{x}, {_}, {z}") 실행 시 {_}가 20으로 나오긴 나옴!
print()

# 첫 번째 값만 변수에 저장하고 나머지는 따로 처리하고 싶을 때: * 기호 사용
x, *rest = (1, 2, 3, 4, 5)      # 첫 번째 값만 x, 나머지는 rest라는 변수에 담긴다
print(f"x: {x}, rest: {rest}")  # 나머지 데이터는 리스트 형태로 패킹됨
print()

"""
    튜플: 불변, () 기호, 딕셔너리 키로 활용 가능!
    리스트: 가변, [] 기호, 딕셔너리 키로 활용하기에는 위험함!
            (리스트는 중복값을 허용하는데 딕셔너리는 키값의 중복을 허용하지 않으므로!)
"""
# 튜플이 딕셔너리에서 키값의 역할을 하는 경우
locations = {
    (35.5451, 126.9750): "서울역",
    (30.5401, 124.9050): "부산역",
 }

