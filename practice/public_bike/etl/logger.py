"""
    로깅 설정

    [로깅 구성 요소]
    - Logger    : 로그를 남길 객체
    - Handler   : 로그가 출력될 공간을 설정
            - StreamHandler : 화면 출력 (표준)
            - FileHandler   : 파일
        (Logger 하나에 여러 Handler를 연결 => 같은 메시지를 여러 곳에 출력 가능)
            - Formatter     : 출력 형식 저장
                             (시간/레벨/내용/형식)
"""
import logging
import os

from datetime import datetime
from .config import LOG_DIR

def setup(name="pipeline", level=logging.INFO):
    """
        화면과 파일에 동시 기록하는 로거 반환

        Args.
            name: 로거 이름
            level: 로그 레벨
        
        Return.
            설정이 완료된 로거 객체
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    path = os.path.join(LOG_DIR, f"{datetime.now():%Y%m%d}.log")

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.handlers.clear()

    fmt = logging.Formatter("%(asctime)s [%(levelname)-7s] %(message)s", "%H:%M:%S")
    console = logging.StreamHandler()
    console.setFormatter(fmt)

    file = logging.FileHandler(path, encoding="utf-8")
    file.setFormatter(fmt)

    logger.addHandler(file)

    return logger
    
