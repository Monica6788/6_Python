"""
    열(컬럼) 다루기
"""
import pandas as pd

from utils.loader import load_csv

pd.set_option('display.width', 130)     # 출력 창 길이 설정

df = load_csv()

# 마지막 거래일 기록만 조회하여 day 변수에 저장. 인덱스 초기화
print(f"{'=' * 33} 마지막 거래일 {'=' * 33}")
last_day = df['date'].max()
day = df[df['date'] == last_day].reset_index(drop=True)
print(day.head())
print()

# 새로운 열(컬럼) 추가
print(f"{'=' * 42} 새 컬럼 추가 {'=' * 42}")
day['range'] = day['high'] - day['low']     # range 컬럼에는 최고가 - 최저가
# 동일한 위치의 컬럼값끼리 자동으로 계산됨
day['range_pct'] = day['range'] * 100 / day['low']
print(day.head())
print()

# 열 삭제 df.drop(columns=[컬럼명, ...])
print(f"{'=' * 20} 열 삭제 df.drop(columns=[컬럼명]) {'=' * 20}")
day['temp'] = 0
print(f"day의 shape: {day.shape}")                     # (107, 12)
day = day.drop(columns=['temp'])
print(f"temp 컬럼 삭제 후 day의 shape: {day.shape}")    # (107, 11)
print()

# 열 이름 변경 df.rename(columns={기존열이름:변경할열이름, ...})
print(f"{'=' * 20} 열 삭제 df.rename(columns={{기존이름:변경할이름}}) {'=' * 20}")
renamed = day.rename(columns={'close': '종가'})
print(renamed.columns)
print()

# .str 접근자
#   문자열 메서드를 모든 행에 일괄 적용할 때 사용
print(f"{'=' * 22} .str 접근자 {'=' * 22}")
print("     : 문자열 메서드를 모든 행에 일괄 적용할 때 사용")

print(f"길이 len() -> {day['code'].str.len()}")
print(f"길이 len() -> {day['code'].str.len().unique().tolist()}")
print(f"슬라이싱 -> {day['code'].str[1:].head(3).tolist()}")     # 코드에서 G 빼고 숫자만
print(f"G00으로 시작하는 종목 코드 개수 -> {day['code'].str.startswith('G00').sum()} 개")
print()

sample = pd.Series(["    가온전자  ", "해피 바이오", "한빛중공업"])
print(f"공백 제거: {sample.str.strip().tolist()}")

sample2 = pd.Series(["52000", "51500", "N/A", "1,240"])
print(f"sample2: {sample2.tolist()}")
print()

# sample2.astype('float64')
# ValueError: could not convert string to float: 'N/A'

converted = pd.to_numeric(sample2, errors='coerce')
# errors='coerce' : 변환 중 오류 발생 시 해당 값을 결측으로 처리
print(converted.tolist())
print(f"결측: {converted.isna().sum()} 개")

c = pd.to_numeric(sample2.str.replace(',', ''), errors='coerce')
print(c.tolist())
print(f"결측: {c.isna().sum()} 개")

print()

"""
    astype은 하나라도 값이 이상하면 전체를 변경할 수 없음.
    to_numeric(errors='coerce')은 오염된 데이터를 강제로 nan(결측)으로 남기고
    나머지는 변경한다.
"""