"""
    Pipeline: 전체 흐름 관리
"""
import time

from . import extract, transform, load
from .config import SOURCE
from .logger import setup

def run():
    """파이프라인 전체 실행 및 성공 여부 반환"""
    logger = setup()

    t0 = time.perf_counter()

    logger.info("=" * 60)
    logger.info("파이프라인 시작")
    logger.info("=" * 60)

    # [1] Extract ----------------------------
    logger.info("[Extract]")
    t = time.perf_counter()

    bike_records, bike_failed = extract.raw_bikes()
    rental_records, rental_failed = extract.raw_rentals()

    if not (bike_records and rental_records):
        logger.error(f" [파이프라인 중단] 수집 결과 없음.")
        return False

    logger.info(f"  bikes  : {len(bike_records):,}건 수집")
    logger.info(f"  rentals: {len(rental_records):,}건 수집")
    logger.info(f"  {time.perf_counter() - t:.1f}초 소요")

    # [2] Transform --------------------------
    logger.info("[Transform]")
    t = time.perf_counter()

    # [3] Load -------------------------------
    logger.info("[Load]")
    t = time.perf_counter()