"""
    Extract : 데이터를 수집하여 원본을 그대로 보관

    - 하지 않는 것: 데이터 정제
"""
import time

import pandas as pd
import requests

from config import (KHLAB_BASE, MAX_PAGES, PAGE_SIZE,
                    TIMEOUT, DELAY, raw_prices_path, ENCODING)

# HTTP 요청 헤더
# => 누가 어떤 목적으로 요청하는지에 대한 정보를 담아둠
#    * User-Agent : 요청을 보내는 클라이언트 이름
#    * X-... : 비표준 헤더 설정.
HEADERS = {
    "User-Agent": "KHLab-Pipeline/1.0 (교육용 실습)",
    "X-Student-Id": "260611"
}

def from_api(logger, max_pages=MAX_PAGES):
    """
        API를 통해 데이터를 수집.
        KH-LAB API에서 데이터를 수집하여 반환.

        Return: (rows, failed)
            rows    : 응답 데이터를 list[dict] 형태로 변환
            failed  : 응답 받지 못한 페이지 번호 목록
    """
    # rows는 수집한 전체 데이터를 담을 list
    rows, failed = [], []

    # 세션 객체를 사용
    # : 동일한 네트워크 연결(TCP Connection)을 유지하며 반복 요청 수행
    with requests.Session() as s:
        # 위에서 정의한 공통 헤더 일괄 적용
        s.headers.update(HEADERS)

        for page in range(1, max_pages + 1):
            try:
                # API 서버에 GET 요청 전송
                # - params
                # : URL 뒤에 ?page=1&limit=100 형태로 자동조합되어 전달
                # - timeout
                # : 서버 응답이 지정된 시간(초) 이상 지연되면 에러 발생 처리
                resp = s.get(f"{KHLAB_BASE}/api/v1/companies",
                             params={"page":page, "limit":PAGE_SIZE},
                             timeout=TIMEOUT)
            except requests.RequestException as e:
                # 네트워크 단절, 타임아웃 등 통신 자체에 실패 시 예외 처리
                # WARNING 레벨로 출력
                logger.warning(f"page {page} 요청 실패: {type(e).__name__}")
                failed.append(page)
                # 예외 처리 후에도 프로그램이 멈추지 않고 동작되도록 처리
                # 즉, 다음 페이지로 계속 진행
                continue

            # 상태코드 확인. 200이 아니면 파싱 작업 패스.
            if resp.status_code != 200:
                logger.warning(f"page {page} 상태코드 {resp.status_code}")
                failed.append(page)
                # 예외 처리 후에도 프로그램이 멈추지 않고 동작되도록 처리
                continue

            # 응답 본문 (JSON 문자열) -> dict 변환
            body = resp.json()
            items = body.get("items") or []

            if not items:
                # 응답 본문이 비어 있을 경우, 더 이상 데이터가 없음.
                # INFO 레벨로 출력
                logger.info(f"page {page} 0건 - 종료")
                break

            # 리스트.extend(추가할_리스트): 리스트 합치기
            rows.extend(items)
            logger.info(f"page {page} {len(items)}건 (누적 {len(rows)})")

            # 요청 간 대기 시간 설정
            time.sleep(DELAY)

        if failed:
            logger.warning(f"실패한 페이지: {failed}")

        # 성공한 데이터 rows와 실패한 페이지 목록 failed 반환
        return rows, failed

def from_csv(logger, path=None):
    """
        CSV에서 데이터를 수집
        API 통신이 불안정하거나, 오프라인 상태일 때 사용

        Args:
            path: CSV 파일 경로. 
                  생략 시 config에 저장된 경로 사용
        Return. (rows, failed)
            rows    : 수집된 데이터 목록
            failed  : 실패 페이지 목록.
                      페이지 정보가 없으므로 빈 list 반환.
    """
    rows, failed = [], []

    # path가 생략되었을 경우(즉, path=None)
    # 원본 파일 경로(raw_prices_path)로 기본 경로 설정
    # path = path if path is not None else raw_prices_path()
    # 위에는 혼자 써본 것, 아래는 실습 코드
    path = path or raw_prices_path()

    # 저장된 데이터를 그대로 유지해서 읽어오기
    # 이 시점에 로그 기록 
    # logger.info()까지만 작성해봤고 아래는 실습코드
    df = pd.read_csv(path, encoding=ENCODING, 
                     dtype=str, keep_default_na=False)
    logger.info(f"{path}로부터 {len(df):,}행 읽음")

    # dict 형태로 반환
    return df.to_dict("records"), []