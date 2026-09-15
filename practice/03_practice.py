"""
    실습용 사이트에서 종목 메뉴 페이지(ssr)의 섹터를 "IT 서비스로 검색한 결과 데이터를 추출"
    (sector가 IT서비스인 목록만 스크래핑)
    - 요청 주소: ??
    TODO 0915(화) 18:00까지 이메일 제출
"""
import requests
from bs4 import BeautifulSoup
from config import BASE, TIMEOUT, HEADERS
from parsers import parse_stocks


