"""
    공통 파서 모듈
"""
# 정규표현식을 쓰기 위한 모듈 re
import re
from bs4 import BeautifulSoup
from config import BASE
# urljoin 함수만 import
from urllib.parse import urljoin

# 텍스트 추출 함수 (node: 컴퓨터 과학에서 네트워크 장치/자료구조의 기본 단위)
def get_text(node, selector, default=""):
    """
        HTML 태그 안에서 '텍스트(글자)'만 안전하게 추출하는 함수

        Args:
            node: 찾을 범위가 되는 HTML
            selector: 찾고자 하는 요소의 CSS 선택자
            default: 요소를 찾지 못했을 때 사용할 기본값
    """
    tag = node.select_one(selector)
    return tag.get_text(strip=True) if tag else default

# 속성 추출 함수
def get_attr(node, selector, attr, default=""):
    """
        HTML 태그 안에서 '속성값(href, src 등)'을 안전하게 추출하는 함수

        Args:
            node: 찾을 범위가 되는 HTML (HTML 요소)
            selector: 찾고자 하는 요소의 CSS 선택자
            attr: 찾고자 하는 요소의 속성명
            default: 찾지 못했을 때 사용할 기본값
    """
    tag = node.select_one(selector)

    # 태그(요소)를 찾지 못했을 경우 def 라인의 매개변수에 미리 받았던 default="" 반환
    if not tag:
        return default

    # 속성을 찾지 못했을 경우 속성의 default가 있어야 하므로 default도 같이 전달
    return tag.get(attr, default)

# 숫자 추출 함수
def get_number(node, selector, default=0):
    """추출된 데이터에서 '숫자'만 깔끔하게 뽑아 반환하는 함수"""
    text = get_text(node, selector)
    numbers = re.sub(r"[^\d]", "", text)    # 숫자가 아닌 문자를 모두 제거
    return int(numbers) if numbers else default

# 실수 추출
def parse_rate(text, default=None):
    """
        부호, 소수점, % 기호가 포함된 텍스트에서
        숫자 부분만 실수(float) 형태로 추출하는 함수
    """
    if not text:
        return default

    # r"": 백슬래시(\)를 문자 그대로 인식시켜주는 Raw String 선언
    # -?: 마이너스 기호가 0개 or 1개라는 뜻
    # [\d.]+: 숫자(\d)나 소수점(.)이 1개 이상 반복되는 덩어리
    m = re.search(r"-?[\d.]+", text)        # Match Object라서 m

    # m.group(): 매치 상자 m에서 실제로 매칭된 문자열 조각만 꺼내기
    return float(m.group()) if m else default

# stock 목록 파서
def parse_stocks(html):
    """
        주식 목록 전체 HTML 문자열을 통해,
        필요한 데이터만 추출하여 딕셔너리 리스트로 반환해주는 함수

        - 동작 순서
        1. 텍스트 형태의 HTML을 BeautifulSoup을 이용하여 DOM 구조로 변환
        2. 목록에 해당하는 컨테이너 단위로 먼저 추출
           (컨테이너: 전체를 감싸는 부모 요소, 실습 코드에서는 tr.stock-row)
        3. 해당 컨테이너에서 이름, 가격, 링크 등을 안전하게 추출한 리스트를 반환
    """
    soup = BeautifulSoup(html, 'lxml')

    results = []
    """
        <tr class="stock-row" data-code="G0001">
            <td class="col-code">G0001</td>
            <td class="col-name"><a href="/stocks/G0001">가온전자</a></td>
            <td class="col-sector">전기전자</td>
            <td class="col-price">9,963 ₲</td>
            <td class="col-change up">+0.27%</td>
            <td class="col-volume">2,020,931</td>
            <td class="col-market"><span class="badge market-main">GX-MAIN</span></td>
        </tr>
        위와 같은  HTML에서 각각의 항목들을 추출
        지금은 연습을 위해 전부 추출했지만 실제 작업할 때는 필요한 값만 추출하면 됨
    """
    for row in soup.select("tr.stock-row"):
        results.append(
            {
                "code": get_text(row, "td.col-code"),    # row가 찾을 범위 (node)
                "name": get_text(row, "td.col-name a"),
                "sector": get_text(row, "td.col-sector"),
                "price": get_number(row, "td.col-price"),
                # change의 key값은 rate로 바꾸어 저장
                # get_text()로 text 먼저 추출, get_text()가 반환한 text를 다시 float으로 parse
                "rate": parse_rate(get_text(row, "td.col-change")),
                "volume": get_number(row, "td.col-volume"),
                "market": get_text(row, "td.col-market span"),
                "link": urljoin(BASE, get_attr(row, "td.col-name a", "href"))
            }
        )
    return results


# 선택한 섹터의 stock 목록 파서 ()
def parse_stocks_by_sector(html, sector="", market="", q=""):
    """
        선택한 섹터의 주식 항목만 리스트에 담아 반환하는 함수
    """
    soup = BeautifulSoup(html, 'lxml')
    results = []
    for row in soup.select("tr.stock-row"):
        if get_text(row, "td.col-sector") == sector:
            results.append({
                "code": get_text(row, "td.col-code"),
                "name": get_text(row, "td.col-name a"),
                "sector": get_text(row, "td.col-sector"),
                "price": get_number(row, "td.col-price"),
                "rate": parse_rate(get_text(row, "td.col-change")),
                "volume": get_number(row, "td.col-volume"),
                "market": get_text(row, "td.col-market span"),
                "link": urljoin(BASE, get_attr(row, "td.col-name a", "href"))
            })
    return results