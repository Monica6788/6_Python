"""
    Extract: 수집 데이터 원본 보관
"""
import pandas as pd

from .config import ENCODING, raw_rentals_path, raw_bikes_path, stations_path
from .logger import setup

logger = setup()

def raw_bikes(logger=logger, path=raw_bikes_path()):
    """
        CSV에서 데이터 수집

        Args.
            path: 파일 경로. 생략 시 stations_path
        
        Returns.
            rows: 수집 데이터 목록
            failed: 실패 페이지 목록 
                    (페이지 정보가 없으므로 빈 리스트 반환)
    """
    df = pd.read_csv(path, encoding=ENCODING,
                     dtype=str, keep_default_na=False)
    logger.info(f"  {path}로부터 {len(df):,}행 읽어옴")

    return df.to_dict("records"), []

def raw_rentals(logger=logger, path=raw_rentals_path()):
    """
        CSV에서 데이터 수집

        Args.
            path: 파일 경로. 생략 시 stations_path
        
        Returns.
            rows: 수집 데이터 목록
            failed: 실패 페이지 목록 
                    (페이지 정보가 없으므로 빈 리스트 반환)
    """
    df = pd.read_csv(path, encoding=ENCODING,
                     dtype=str, keep_default_na=False)
    logger.info(f"  {path}로부터 {len(df):,}행 읽어옴")

    return df.to_dict("records"), []

def stations(logger=logger, path=stations_path()):
    """
        CSV에서 데이터 수집

        Args.
            path: 파일 경로. 생략 시 stations_path
        
        Returns.
            rows: 수집 데이터 목록
            failed: 실패 페이지 목록 
                    (페이지 정보가 없으므로 빈 리스트 반환)
    """
    df = pd.read_csv(path, encoding=ENCODING)
    logger.info(f"  {path}로부터 {len(df):,}행 읽어옴")

    return df.to_dict("records"), []