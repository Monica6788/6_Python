"""
    실습용 사이트에서 종목 메뉴 페이지(ssr)의 섹터를 "IT 서비스로 검색한 결과 데이터를 추출"
    (sector가 IT서비스인 목록만 스크래핑)
    - 요청 주소: ??
    TODO 0915(화) 18:00까지 이메일 제출
"""
import requests
from bs4 import BeautifulSoup
from config import BASE, TIMEOUT, HEADERS
from parsers import parse_stocks, parse_stocks_by_sector

resp = requests.get(f"{BASE}/stocks?sector=S08&market=&q=", headers=HEADERS, timeout=TIMEOUT)
resp.raise_for_status()

html = resp.text

soup = BeautifulSoup(html, 'lxml')

it_stocks = parse_stocks(html)
print("=" * 75)
print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>12}{'등락률':>9}")
print("-" * 75)
for s in it_stocks:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")
print()

# 섹터 선택하여 조회하기 전 전체 목록 페이지에서 추출
print(f"{'=' * 32} 추가 학습 {'=' * 32}")
resp2 = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
resp2.raise_for_status()

html2 = resp2.text

it_service_stocks = parse_stocks_by_sector(html2, "IT서비스")
print(f"{'코드':<8}{'종목명':<14}{'섹터':<10}{'현재가':>12}{'등락률':>9}")
print("-" * 75)
for s in it_service_stocks:
    print(f"{s['code']:<8}{s['name']:<14}{s['sector']:<10}{s['price']:>12}{s['rate']:>9}")
