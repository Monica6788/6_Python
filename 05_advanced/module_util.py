"""
    import 하기 위한 모듈
    - 직접 실행할 수도 있고, 다른 파일에서 가져다(import) 사용할 수도 있음
"""
BASE_URL = "https://kh-academy.co.kr/"

def clean_price(text):
    """`1,000원` 같은 문자열에서 정수부분만 추출하는 함수 - > 1000"""
    return int(text.replace(",", "").replace("원", "").strip())

def to_code(number):
    """
        특정 숫자가 전달되면 앞에 0을 채워 6자리 문자열로 반환하는 함수
    """
    # {number:06d}: f-string 옵션 중 하나로, 6자리를 채워 앞 부분에 0을 추가함
    return f"{number:06d}"

print("module_util 모듈이 로드되었습니다.")