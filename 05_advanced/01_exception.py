"""
    예외 처리
    try / except / else / finally
"""
# 함수 정의: divide
#   데이터를 하나 전달 받아 정수로 변환하고,
#   변환된 값으로 60을 나눈 결과를 출력
def divide(text):
    try:
        num = int(text)
        result = f"60 / {num} = {60 / num}"
        # print(result)
    except ValueError:
        print(f"\"{text}'\" : 수로 변환할 수 없습니다.")
    except ZeroDivisionError:
        print(f"\"{text}\": 0으로는 나눌 수 없습니다.")
    except Exception as e:      # 별칭 부여
        print(f"{text} : {e}")
    else:       # 예외가 없을 때 실행되는 블록
        print(result)
    finally:
        pass    # 예외 발생 여부와 관계 없이 항상 실행되는 블록

for t in ["100", "60", "abc", "0", "+20", "-30"]:
    divide(t)
print()

print("=" * 60)
print(f"{'사용자 정의 예외 / 예외 발생시키기 (raise)':^46}")
print("=" * 60)
# 사용자 정의 예외 / 예외 발생시키기 (raise)
class NoBalanceError(Exception):
    """잔액 부족 예외"""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"잔액이 부족합니다. (현재 잔액: {balance:,}원, 요청 금액: {amount:,}원)")

class InvalidAmountError(ValueError):
    """금액이 잘못된 경우 예외"""

class Account:
    """은행 계좌를 나타내는 클래스"""
    def __init__(self, owner, balance = 0):
        self.owner = owner
        self.balance = balance

    def withdraw(self, amount):
        """
            출금 메서드

            Args:
                amount (int): 출금 금액
            
            Returns:
                amount (int): 출금 금액
        """
        if amount <= 0:
            raise InvalidAmountError("출금액은 0보다 커야 합니다.")
        if amount > self.balance:
            raise NoBalanceError(self.balance, amount)
        self.balance -= amount
        return amount

    def __str__(self):
        return f"{self.owner}님의 잔액은 {self.balance:,}원입니다."

park = Account("박민성", 30000)
print(park)

for amount in [5000, 60000, -3000]:
    try:
        park.withdraw(amount)
    except InvalidAmountError as ivae:
        print(ivae)
    except NoBalanceError as nbe:
        print(nbe)
    else:
        print(f"{amount:,}원이 출금되었습니다. (잔액: {park.balance:,}원)")
        

# TODO: 마지막 반복문에서 발생되는 예외를 처리