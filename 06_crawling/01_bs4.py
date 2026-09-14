"""
    BeautifulSoup
    : HTML 및 XML (Markup Language) 문서에서
      원하는 데이터를 쉽게 추출할 수 있게 해주는 스크래핑 라이브러리
    
    1. requests로 요청 후 문자열(html, xml)을 응답 받음
    2. bs4의 find, select를 활용하여 특정 텍스트를 추출
"""
import requests
# ModuleNotFoundError: No module named 'requests'
# --> 해당 모듈 설치 필요! pip install requests
from bs4 import BeautifulSoup
from config import BASE, TIMEOUT, HEADERS

resp = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()   # 200이 아니면 예외를 발생시켜줌

print(f"상태코드: {resp.status_code}")

html = resp.text
print(f"{BASE}/stocks  [{resp.status_code}] {len(html):,}자")

print("-" * 60)

# 문자열 --> 태그 구조
# pip install beautifulsoup4 lxml 설치 후 import

# bs4는 문자열을 DOM 트리처럼 다룰 수 있게 만들어 줌
# html과 파서(parser) 도구인 lxml을 매개변수로 전달
soup = BeautifulSoup(html, 'lxml')

# .title.text로 헤드 내의 title 태그 내부 텍스트 탐색 가능
# <title> 태그가 없을 경우에 대비하여, 안전하게 삼항 연산 형태로 접근
print(f"title --> {soup.title.text if soup.title else '없음'}")

# 기존에 JavaScript를 통해 DOM을 조작한 것처럼 bs가 같은 역할을 함.

# select : CSS 선택자를 사용하여 해당 요소들을 반환. 없는 경우 [] 반환.
# select_one: CSS 선택자를 사용하여 해당 요소 1개 반환. 없는 경우 None 반환.
rows_select = soup.select("tr.stock-row")
print(f"tr.stock-row 개수: {len(rows_select):,}건")

first = soup.select_one("tr.stock-row")
price_tag = first.select_one("td.col-price")
print(f"td.col-price text : {price_tag.text}")
# f-string에서 !r을 사용하면 repr()이 호출되어
# 숨겨진 공백 (\n, \t 등)까지 그대로 출력해줌!
print(f"td.col-price text : {price_tag.text!r}")    # ''로 감싸져서 표시됨

# get_text() 메서드 뒤에도 동일하게 사용 가능
print(f"td.col-price text : {price_tag.get_text()!r}")

# get_text() 메서드에 strip 옵션을 True로 설정하면 공백을 제거하고 가져올 수 있음.
print(f"td.col-price text : {price_tag.get_text(strip=True)!r}")
print("-" * 60)

# 속성값을 추출 --> get() 메서드
name_link = first.select_one("td.col-name a")
print(f"name_link['href'] : {name_link['href']}")
print(f"name_link.get('href') : {name_link.get('href', '없음')}")

# 첫 번째 행의 전체 데이터를 추출 TODO 7일차에 계속!