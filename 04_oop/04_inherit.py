"""
    상속과 다형성
"""
class Account:
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance      # 캡슐화 생략!

    def withdraw(self, amount):
        if amount > self.balance:
            print("잔액이 부족합니다.")
            return

        self.balance -= amount
        return amount

    def info(self):
        return f"{self.owner}님의 잔액은 {self.balance:,}원입니다."

# 상속 -> class 클래스명(부모클래스명):
# super() 부모 클래스(객체)
class SavingsAccount(Account):
    # rate는 기본값 없으면 balance보다 앞에 작성
    def __init__(self, owner, balance = 0, rate = 0.03):
        # super().__init__ : 자식이 부모의 초기화 기능을 덮어쓰므로(오버라이딩)
        #       부모의 속성을 물려받기 위해 예외적으로 던더 메서드를 직접 호출함.
        super().__init__(owner, balance)    # 부모 생성자 호출
        self.rate = rate

    def add_interest(self):
        interest = int(self.balance * self.rate)
        self.balance += interest
        return interest

    def info(self):         # 메서드 오버라이딩 (재정의)
        return f"{super().info()} / 이율 {self.rate * 100}%" 

ko = SavingsAccount("고영은", 2000000)
print(f"info: {ko.info()}")
print(f"이자 지급: {ko.add_interest():,}원")
print(f"info : {ko.info()}")
print()

class CheckingAccount(Account):
    FEE = 500       # 수수료

    # 생성자를 정의하지 않음
    # => Account(부모 타입) 생성자를 기준으로 생성할 수 있게 됨
    
    def withdraw(self, amount):
        total = amount + self.FEE

        if total > self.balance:
            print("잔액이 부족합니다.")
            return

        self.balance -= total
        return amount

    def info(self):
        return f"{super().info()} / 수수료 : {self.FEE}원"

acc_list = [
    Account("김솔음", 20000000),
    SavingsAccount("최요원", 3000000),
    CheckingAccount("류재관", 5000000)
]

for acc in acc_list:
    print(f"{acc.info()}")

# 덕 타이핑 (Duck Typing)  -- "오리처림 행동하면 오리다!"라는 논리
#   상속 관계가 없어도 같은 메서드를 가지면 동일하게 취급하는 특징