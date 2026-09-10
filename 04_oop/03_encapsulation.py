"""
    캡슐화
    
    클래스 내부의 데이터를 임의로 접근할 수 없게 하고 (정보 은닉)
    데이터와 처리 메서드를 모아서 관리함 (데이터와 기능의 결합)

    - 인스턴스 변수명 앞에 언더바를 추가하여 "접근하지 말자"라는 표시 (관례)
    - @property, @필드명.setter를 통해 getter, setter를 정의
"""
# 네이밍 규칙 (_필드명 / __필드명) -> 파이썬에는 private 접근제한자 없음
class Account:
    def __init__(self, owner, balance = 0):
        self.owner = owner          # public
        self._bank_code = "005"     # 접근이 가능하지만 "접근하지 말자!"
        self.__balance = balance    # 네임맹글링 적용

gaerong = Account("이자헌", 50000000)
print(f"owner (예금주) : {gaerong.owner}")
print(f"_bank_code : {gaerong._bank_code}")     # 오류 x (접근은 가능). 직접 접근하지 말자는 약속!
# print(f"__balance : {gaerong.__balance}")     # AttributeError 발생

print(f"실제 이름: {[k for k in vars(gaerong)]}")
print(f"_Account__balance : {gaerong._Account__balance:,}원")

# 네임맹글링 (name mangling)
# `__필드명` 형태의 변수는 `_클래스명__필드명` 형태로 변환되어 직접 접근을 차단함
# 변환된 이름으로 접근이 가능하지만, 사용을 권장하지는 않음
print("=" * 60)

# @property: 메서드를 속성(필드)처럼 사용하게 해주는 데코레이터
class SafeAccount:
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.__balance = balance

    # `__balance`의 getter
    @property
    def balance(self):
        return self.__balance

    # `__balance`의 setter
    @balance.setter
    def balance(self, value):
        """setter"""
        if value < 0:               # 잔고가 0보다 작으면
            self.__balance = 0      # 0으로 초기화 후
            return                  # 메서드 종료

        self.__balance = value      # 아니면 value로 초기화

    @property
    def info(self):
        return f"{self.owner}님의 현재 잔고는 {self.__balance:,}원입니다."

sa_eun = SafeAccount("은하제", 6000000)

print(f"sa_eun.balance : {sa_eun.balance:,}원")     # getter 사용
sa_eun.balance = 12000000                       # setter 사용
print(f"sa_eun.balance : {sa_eun.balance:,}원")
# sa_eun.balance = - 30000
# print(f"sa_eun.balance : {sa_eun.balance:,}원")     # 음수값이 들어가서 0으로 초기화

print(f"sa_eun.info : {sa_eun.info}")