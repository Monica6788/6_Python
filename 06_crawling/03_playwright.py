import requests
from config import BASE, TIMEOUT, HEADERS
from parsers import parse_stocks

# ssr: server side rendering. 서버에서 완성된 화면을 응답.
# csr: client side rendering. 빈 HTML을 서버로부터 응답 받고,
#                             JavaScript를 통해 데이터를 화면에 표시.

ssr = requests.get(f"{BASE}/stocks", headers=HEADERS, timeout=TIMEOUT)
csr = requests.get(f"{BASE}/csr/stocks", headers=HEADERS, timeout=TIMEOUT)

print(f"{'경로':<20}{'상태':<8}{'본문 길이':>12}")
print(f"{'/stocks (SSR)':<20}{ssr.status_code:<8}{len(ssr.text):>12}")
print(f"{'/csr/stocks (CSR)':<20}{csr.status_code:<8}{len(csr.text):>12}")

# 렌더링 방식에 따라 <body>가 비어 있을 수 있는데, csr일 때는 bs로 파싱할 수 없음

# csr 본문 확인
# for line in csr.text.strip().split("\n"):
#     print(f"{line}")

KEYWORD = '가온전자'
print(f"ssr --> {KEYWORD in ssr.text}")     # True
print(f"csr --> {KEYWORD in csr.text}")     # False
print("=" * 160)

"""
    Playwright
    브라우저 자동화를 통해 동적 페이지 데이터를 수집을 지원하는 도구

    - 기본 구조
    Browser: 브라우저 (프로세스)
    Context: 쿠키, 캐시 등이 저장되는 공간
    Page: 탭 (우리가 원하는 동적 페이지로 이동 가능)
"""

# Playwright 동기 방식 API
from playwright.sync_api import sync_playwright

print(f"동적 페이지 수집: Playwright")

with sync_playwright() as p:
    # browser: 크롬을 실행
    # headless=True로 설정 시 창이 보이지 않음
    browser = p.chromium.launch(headless=True)

    # context: 창 하나에 해당. 쿠키, 캐시가 독립적으로 보관됨.
    #          독립적으로 보관되므로 시크릿 창이라고 볼 수 있음.
    context = browser.new_context(locale="ko-KR",
                                  viewport={"width": 1280, "height": 720})

    # page: 실제로 조작하기 위한 탭 하나
    page = context.new_page()

    # page.route(패턴, 처리함수) : 특정 패턴의 요청을 가로채어 직접 처리하는 함수
    # route.abort() : 요청을 취소시키는 함수 (이미지, 폰트 등 필요 없는 데이터 빼고 요청)
    # route.continue_() : 요청을 그대로 진행시키는 함수
    page.route(
        # 모든 URL에서 요청을 가로채서 처리
        "**/*",
        lambda route: route.abort() if route.request.resource_type in {"image", "font", "media"}
                                    else route.continue_()
    )

    # wait_until
    #   - domcontentloaded: HTML을 다 읽고 DOM트리가 만들어진 시점 (JS 실행 전)
    #   - load: 이미지를 포함한 모든 리소스가 로드된 시점 (기본값) => 느림...
    page.goto(f"{BASE}/csr/stocks", wait_until="domcontentloaded")

    # wait_for_selector() : 해당 선택자가 DOM에 그려질 때까지 대기
    page.wait_for_selector("tr.stock-row")

    # 요소 선택
    count = page.locator("tr.stock-row").count()
    print(f"렌더링 후 가져온 행의 개수: {count}개")

    # content(): DOM을 문자열로 변환
    html = page.content()
    # print(f"page.content: {html}")

    # html 문자열을 page.content()로 가져왔으니 이걸 다시 parse_stocks 함수에 전달
    items = parse_stocks(html)

    # 다 가져온 후 창 닫기
    browser.close()

# 5개만 출력 (슬라이싱)
for data in items[:5]:
     print(f"{data['code']} | {data['name']} : {data['price']}원")


"""
    * headless=False, slow_mo=1000 (각 동작을 1초씩 늦추기)
        : 화면을 직접 보면서 확인 가능

    * 스크린샷, HTML 저장
        page.screenshot(path=".../screenshot.png", full_page=True)
        open("capture.html", "w", encoding="utf-8").wrtie(page.content())
    
    * 브라우저 콘솔
        page.on("console", lambda m: print(f"[BROWSER] {m.text}"))
"""


