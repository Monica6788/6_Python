"""
    목록 파싱
"""
# 파이썬에서 웹 서버로 HTTP 요청을 보내는 라이브러리 requests
import requests, json, csv
from bs4 import BeautifulSoup

from config import BASE, TIMEOUT, HEADERS
from parsers import get_text, parse_stocks

resp = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()     # 응답 코드가 200이 아니면 예외를 발생시키는 메서드

html = resp.text

soup = BeautifulSoup(html, 'lxml')

row = soup.select_one("tr.stock-row")
# row.select_one("td.test").text       # 해당 클래스 부재 시 출력 확인용
# => AttributeError: 'NoneType' object has no attribute 'text'

# 방어1) try-except 구문으로 감싸서 처리
try:
    row.select_one("tr.test").text
except Exception as e:
    print(f"오류 발생: {e}")

# 방어2) parsers.py에 정의된 함수 사용하기
print(f"{get_text(row, 'tr.test')}")    # default = ""라서 빈 문자열만 출력됨
print("=" * 60)

stocks = parse_stocks(html)

print(f"{'코드':<8} {'종목명':<14} {'섹터':<10} {'현재가':>12} {'등락률':>9}")
print("-" * 80)
for s in stocks:
    print(f"{s['code']:<8} {s['name']:<14} {s['sector']:<10} {s['price']:>12} {s['rate']:>9}")
print("=" * 80)

# 파일로 저장
# json
# csv => 상품명,가격,재고
#       아이폰,300000,20

# json 저장하기
def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_json(stocks, "stocks.json")
# 경로를 따로 지정하지 않을 경우, 현재 터미널 위치(실행하는 위치)에 저장

# csv 저장하기
def save_csv(data, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        # 첫 번째 데이터의 key값 목록만 fieldnames로 설정
        # fieldnames -> 컬럼 순서
        writer = csv.DictWriter(f, fieldnames=data[0].keys())

        writer.writeheader()   # csv 파일 맨 첫 줄에 컬럼 이름들로 씀
        writer.writerows(data)  # 딕셔너리 리스트 전체를 각가의 행으로 작성(기록)

save_csv(stocks, "stocks.csv")