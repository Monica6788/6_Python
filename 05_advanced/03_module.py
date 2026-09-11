"""
    모듈 / 패키지
"""
# 모듈 import
# 현재 파일에서 다른 파일(.py)에 정의된 변수/함수/클래스 등을 가져다 쓰기 위해 사용

# 모듈 전체를 가져오기
print("=" * 60)
print(f"{'모듈 전체를 가져오기: import 모듈명':^46}")
print("=" * 60)
import module_util

print(f"3,000원 ---> {module_util.clean_price('3,000원')}")
print()

# 별칭 부여
print("=" * 60)
print(f"{'별칭 부여: import 모듈명 as 별칭':^46}")
print("=" * 60)
import module_util as util

print(f"별칭 util로 함수 호출")
print(f"300,000원 ---> {util.clean_price('300,000원')}")
print()

# 특정 항목만 가져오기
print("=" * 60)
print(f"{'특정 항목만 가져오기: from 모듈명 import 함수(변수)명':^42}")
print("=" * 60)
from module_util import BASE_URL, to_code

print(f"to_code ---> {to_code(7979)}")
print(f"BASE_URL ---> {BASE_URL}")
print()

# 별칭 부여
print("=" * 60)
print(f"{'from 모듈명 import 함수(변수)명 as 별칭':^46}")
print("=" * 60)
from module_util import clean_price as cp

print("별칭 cp로 clean_price 함수 호출")
print(f"39,800원 ---> {cp('39,800원')}")
print()
