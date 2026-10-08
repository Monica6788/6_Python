"""
    Transform: 데이터 정제, 계산, 검증
"""
import pandas as pd

from .extract import from_csv

BIKES_NUM_COLS = ["gear_count", ]


def validate(df, logger):
    """
        검증
    """