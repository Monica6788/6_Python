"""
    연습문제 5 - 케글
"""
import pandas as pd

from practice_05.loader import load_csv

"""
    문제 1. 데이터 구조 파악

    데이터의 행 수, 열 수를 출력하시오.
    결측치가 있는 컬럼을 찾아 개수를 함께 출력하시오.
"""
df = load_csv()
df.info()