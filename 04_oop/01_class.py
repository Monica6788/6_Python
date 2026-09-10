"""
    클래스와 객체

    - 기본 형태
    class 클래스명:
        # 생성자
        def __init__(self):
            self.필드명 = 값

        # 메서드
        def 메서드명(self):
            pass # 실행할 내용
"""
class Account:
    # 생성자
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    # 메서드
    def deposit(self, amount):
        self.balance += amount
        return self.balance

# 객체 생성
acc = Account("Nero", 50000)

print(f"owner (예금주): {acc.owner}")
print(f"balance (잔고): {acc.balance}원")

print(f"deposit (입금 후 잔고): {acc.deposit(7500)}원")
print("=" * 60)

# 인스턴스 변수 vs 클래스 변수
class Member:
    # 클래스 변수: 모든 인스턴스 객체가 공유하는 변수
    team_name = "에스파"
    count = 0

    # 생성자
    def __init__(self, name):
        self.name = name        # 인스턴스 변수
        # count += 1            # 이렇게 쓰면 지역변수가 되므로 클래스명을 붙여서 작성
        Member.count += 1

m1 = Member("카리나")
m2 = Member("윈터")
m3 = Member("닝닝")
m4 = Member("지젤")

print(f"m1.name : {m1.name}")
print(f"m2.name : {m2.name}")
print(f"m3.name : {m3.name}")
print(f"m4.name : {m4.name}")
print()

print(f"m1.team_name : {m1.team_name}")
print(f"m2.team_name : {m2.team_name}")
print(f"m3.team_name : {m3.team_name}")
print(f"m4.team_name : {m4.team_name}")
print()

print(f"count : {Member.count}명")
print()

m1.team_name = "Aespa"
# 인스턴스에 클래스변수명으로 값을 대입할 경우,
# 클래스 변수를 변경하는 것이 아니라 새로운 인스턴스 변수를 생성함.
print(f"m1.team_name : {m1.team_name}")
print(f"Member.team_name : {Member.team_name}")     # 클래스 변수 자체는 변경되지 않음!
Member.team_name = "Aespa"      # 클래스명으로 접근해야 클래스 변수의 값을 변경할 수 있음.
print(f"Member.team_name : {Member.team_name}")
print()