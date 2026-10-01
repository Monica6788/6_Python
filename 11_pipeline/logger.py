"""
    로깅 설정
    
    [단순 출력(print) 대신 로깅(logging)을 사용하는 이유]
    - 레벨 구분이 없음.
        DEBUG/INFO/WARNING/ERROR/...로 중요도를 나눌 수 있음.
    - 화면에만 메시지가 남음.
        자동으로 실행되는 프로그램에는 화면이 없어 메시지가 사라짐.
    - 출력 시간을 통해 직접 제시해야 함.
        포맷을 통해 자동으로 출력할 수 있음.

    [로깅 구성 요소]
    - Logger    : 로그를 남길 객체. logger.info(...)
    - Handler   : 로그를 어디에 출력할 것인지 설정.
            StreamHandler : 화면 (표준 출력)
            FileHandler   : 파일
        Logger 하나에 여러 Handler를 연결하면 같은 메시지를 여러 곳에 출력할 수 있음.
    - Formatter : 출력 형식 설정. 시간/레벨/내용/형식을 지정.
"""
import logging
import os

from datetime import datetime
from config import LOG_DIR

def setup(name="pipeline", level=logging.INFO):
    """
        화면과 파일에 동시에 기록하는 로거를 만들어 반환

        Args:
          - name : 로거 이름. 
                getLogger(name)으로 동일한 로거를 반환 가능.
          - level: 로그 레벨.
                레벨 순서 (오름차순)
                DEBUG < INFO < WARNING < ERROR < CRITICAL
        
        Return:
          설정이 완료된 Logger 객체
    """
    # getLogger(name)
    # : 프로그램 내에서 이름(name)이 같다면
    #   언제 어디서 호출해도 항상 똑같은 단 하나의 로거(Logger) 객체 반환
    #  (싱글톤 패턴과 유사함. 하나 가지고 돌려 쓰기)

    # 로그 폴더 생성 (있으면 스킵 - exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)

    # 저장될 로그 파일 설정
    # %Y%m%d : 형식 설정 (YYYYmmdd.log와 같이 저장됨.)
    path = os.path.join(LOG_DIR, f"{datetime.now():%Y%m%d}.log")

    # 로거 객체 생성
    logger = logging.getLogger(name)

    # 로그 레벨 설정
    logger.setLevel(level)

    # 핸들러 초기화
    logger.handlers.clear()
    # --> 함수(setup)가 여러 번 호출될 경우
    #     동일한 메시지가 여러 번 출력될 수 있음.

    # 출력 형식 설정
    fmt = logging.Formatter("%(asctime)s [%(levelname)-7s] %(message)s", "%H:%M:%S")
    # %(asctime)s      : 로그가 기록된 시간. 
    #                    두 번째 인자인 (%H:%M:%S) 형식으로 표시.
    # %(levelname)-7s  : 로그 레벨 이름 (INFO, ERROR, ...)
    #             -7s  : 7자리 왼쪽 정렬.
    # %(message)s      : 실제 로그 메시지 내용.

    # 스트림 핸들러 객체 생성
    # [StreamHandler] => 화면에 출력 (표준 출력)
    console = logging.StreamHandler()
    console.setFormatter(fmt)

    # 스트림 핸들러를 로거에 등록
    logger.addHandler(console)

    # 파일 핸들러 객체 생성
    # [FileHandler] => 파일 출력
    file = logging.FileHandler(path, encoding="utf-8")
    file.setFormatter(fmt)

    # 파일 핸들러를 로거에 등록
    logger.addHandler(file)

    return logger
