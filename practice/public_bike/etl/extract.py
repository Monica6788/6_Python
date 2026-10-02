"""
    Extract: 수집 데이터 원본 보관
"""
import time
import pandas as pd

from .config import (raw_prices_path, TIMEOUT, ENCODING)

def from_csv(logger, path=None):
    """
        CSV에서 데이터 수집

        Args.
            path: 파일 경로. 생략 시 config에 저장된 기본 경로
        
        Returns.
            rows: 수집 데이터 목록
            failed: 실패 페이지 목록 
                    (페이지 정보가 없으므로 빈 리스트 반환)
    """
    path = path or 