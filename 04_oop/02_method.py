"""
    메서드: 클래스 내의 함수

    - 종류
    1) 인스턴스 메서드
    2) 클래스 메서드: @classmethod
    3) 정적 메서드: @staticmethod
"""

class Account:
    bank_name = "KH 은행"
    MIN_DEPOSIT = 1000      # 상수처럼 쓰자는 약속으로 대문자 네이밍

    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    # 인스턴스 메서드: 객체의 데이터를 다룸. 첫 번째 매개변수는 self
    def deposit(self, amount):
        self.balance += amount
        return self.balance

    # 클래스 메서드: 클래스 자체를 다룸. 첫 번째 매개변수는 cls
    # @classmethod 데코레이터 지정
    @classmethod
    def from_dict(cls, data):
        """딕셔너리로부터 객체를 생성하는 메서드"""
        # data라는 딕셔너리에서 "owner"와 "balance"를 꺼내어 와서 쓰기.
        # balance는 지정된 기본값이 있으므로, 딕셔너리의 정보에 balance가 누락되어 있더라도
        # 안전하게 기본값을 채워 넣기 위해 get("key", 기본값)메서드 사용.
        # 예금주 이름은 필수 정보이므로 name의 value가 비어 있으면 계좌를 만들 수 없도록
        # 에러를 발생시키기 위해 data["owner"] 형태로 작성.
        return cls(data["owner"], data.get("balance", 0))

    # 정적 메서드: 객체, 클래스와 무관한 기능을 담당하는 메서드 (유틸리티)
    # @staticmethod 데코레이터 지정
    @staticmethod
    def is_valid_amount(amount):
        return amount >= Account.MIN_DEPOSIT

kim = Account("김솔음", 1000000)
# 인스턴스 메서드 호출
print(f"deposit 입금 후 {kim.owner}님의 잔고 --> {kim.deposit(56700):,}원")
print()

# 클래스 메서드 호출 (딕셔너리 전달)
lee = Account.from_dict({"owner": "이성해", "balance": 800000})
print(f"owner (예금주) : {lee.owner}님, balance (잔고): {lee.balance:,}원")
print()

# 정적 메서드 호출
print(f"amount : 6000 -> {Account.is_valid_amount(6000):,}")
print(f"amount : 300 -> {Account.is_valid_amount(300):,}")
print()

# if문으로 유효성 검증 로직 작성 가능
# amount = int(input("입금할 금액을 입력하세요: "))
# if Account.is_valid_amount(amount):
#     print(f"deposit --> {acc2.deposit(amount)}")
# else:
#     print(f"최소 금액(1000원) 미만은 입금할 수 없습니다.")


# from_dict 활용
response = [
    {"owner": "고영은", "balance": 1000000},
    {"owner": "강이학"},
    {"owner": "브라운", "balance": 87650000}
]

accounts = [Account.from_dict(item) for item in response]

for a in accounts:
    print(f"{a.owner}님의 잔고는 {a.balance:,}원입니다.")

# from_dict를 활용하면 딕셔너리 구조를 자연스럽게 클래스에 넘겨서 객체 생성 가능
# 데이터 구조가 변경되거나 메서드를 수정하는 경우 새로 정의하여 대응 가능

