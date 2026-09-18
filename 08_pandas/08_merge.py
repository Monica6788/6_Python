"""
    merge (SQL의 JOIN과 유사)
"""
import pandas as pd

from utils.loader import load_prices, load_companies

prices_df = load_prices()
companies_df = load_companies()         # 정제본
raw_comp_df = load_companies(True)      # 오염본

print(f"prices_df : {len(prices_df)} 건")
# print(companies_df.head())
# print(companies_df.columns)
"""
Index(['code', 'name', 'sectorCode', 'sectorName', 'market', 'listedDate',
       'ceo', 'address', 'employeeCount', 'listedShares', 'marketCap'],
      dtype='str')
"""
print(f"중복 제거한 섹터 개수 : {companies_df['sectorCode'].nunique()} 개")
print(f"종목 개수 : {len(companies_df)} 개")

"""
    시세 (prices) 90_000행에 섹터 이름을 매번 저장하면?
        같은 문자열이 수천 번 반복될 것임
        => 분리해서 저장하고 식별 코드로 연결해줌! (정규화)

    저장할 때는 나누고, 분석할 때는 합쳐서 진행!
    = 나누어져 있는 데이터를 다시 붙여주는 것: merge
"""
# merge
#   left_df.merge(righ_df, on="기준열", how="방식")
#   => 두 df의 기준열을 모두 가진 새로운 DataFrame이 반환됨
#   - how: "inner", "left", "right", "outer"

# print(prices_df.head(1))
# print(companies_df.head(1))
# => 'code' 컬럼을 사용하여 merge

# prices_df + companies_df
# merged_df = prices_df.merge(companies_df, on="code")
# print(f"prices_df + companies_df :: how='inner(기본값)'")
# print(f"- prices_df : {prices_df.shape}")       # (90_000, 9)
# print(f"- merged_df : {merged_df.shape}")       # (90_000m 19)
# print()

merged_df = prices_df.merge(companies_df, on="code", how="left")
print(f"prices_df + companies_df :: how='left'")
print(f"- prices_df : {prices_df.shape}")       # (90_000, 9)
print(f"- merged_df : {merged_df.shape}")       # (90_000m 19)
print()

p2 = prices_df.head(3).copy()
p2['name'] = '시세데이터_이름'
m2 = p2.merge(companies_df[['code', 'name']], on='code')
print(m2)       # name_x name_y로 출력됨
# 열 이름이 동일한 경우 _x,  _y가 붙은 것을 확인 가능
print()

# - suffixes: 양쪽에 같은 이름의 열이 있을 때 붙일 이름 지정
#   left_df.merge(right_df, on="기준컬럼명", how="", suffixes=("_left", "_company"))
m3 = p2.merge(companies_df[['code', 'name']], on='code', suffixes=("_price", "_company"))
print(m3)
# name_price name_company로 출력됨
print()

# 간혹, merge에서 key가 안 맞는 경우가 있음
# 1. 문자열에 공백이 있는 경우 동일한 값이 아님
#    앞뒤 공백이 있는 경우 (blank_edge)
blk_edge = (raw_comp_df['name'] != raw_comp_df['name'].str.strip()).sum()

#   중간에 공백이 있는 경우 \S: 문자, \s: 공백
blk_mid = raw_comp_df['name'].str.contains(r"\S\s+\S", regex=True).sum()

print(f"{'=' * 20} 공백 체크 {'=' * 20}")
print(f"양끝 공백: {blk_edge} 건")
print(f"중간 공백: {blk_mid} 건")

# 2. 대소문자
print(f"{'=' * 18} 대소문자 체크 {'=' * 18}")
print(f"market 종류: {raw_comp_df['market'].nunique()} 개 :"
      f" {raw_comp_df['market'].unique()}\n")
print(f"upper() 후: {raw_comp_df['market'].str.upper().unique()}\n")

# 3. 전각문자
print(f"{'=' * 18} 전각문자 체크 {'=' * 18}")

def has_fullwidth(s):
    """
        전각문자가 하나라도 있으면 True 반환

        ord(문자) : 해당 문자의 유니코드 번호 반환
            0xFF01 ~ 0xFF5F : 전각 영문, 기호
            0x3000          : 공백
    """
    # s라는 문자열을 받아서 전부 한 글자씩 뜯은 후, 각각의 글자 ch에 대하여
    # 전각문자를 포함하는지 검사하는 것
    return any( (0xFF01 <= ord(ch) <= 0xFF5F) or (ord(ch) == 0x3000) for ch in str(s) )

# map(함수) : 대상 하나하나에 함수를 적용한 반환값으로 새롭게 동일한 타입으로 반환
#             (대상이 시리즈였다면 시리즈로 반환해주는 것!)
fw = raw_comp_df[raw_comp_df['name'].map(has_fullwidth)]
print(f"{len(fw)} 건\n")

# 4. 타입 불일치
print(f"{'=' * 18} 타입 불일치 {'=' * 18}")
c1 = companies_df.copy()
c1['code_num'] = c1['code'].str.replace("G", "").astype("int64")

p1 = prices_df.head(100).copy()
# 타입 불일치 시키려고 타입변환 안 함
p1['code_num'] = p1['code'].str.replace("G", "")

print(f"c1: {c1['code_num'][0]} {c1['code_num'].dtype}")    # 1 int64
print(f"p1: {p1['code_num'][0]} {p1['code_num'].dtype}")    # 0001 str

# r1 = p1.merge(c1, on="code_num")
# print(r1)
# ValueError: You are trying to merge on str and int64 columns for key 'code_num'.
#             If you wish to proceed you should use pd.concat
# 기준 열의 타입이 다르면 merge 시에 오류 발생!
print()

# outer merge를 활용하여 매칭되지 않은 데이터를 확인 가능

# 특정 종목(코드가 G0001인 종목)을 제외
part = companies_df[companies_df['code'] != "G0001"]
chk = prices_df.merge(part, on="code", how="outer", indicator=True)
# indicator=True: 각 행이 어느 쪽에서 왔는지 표시! ('_merge' 컬럼이 추가됨)
print(f"{chk['_merge'].value_counts()}")    # value_counts() 값별로 개수 확인
"""
    _merge
    both          89250         양쪽에 존재 (즉, 키가 일치한다)
    left_only       750         왼쪽(prices_df)에만 존재, 왼쪽에서 온 키
    right_only        0         오른쪽(part)에만 존재, 오른쪽에서 온 키
    Name: count, dtype: int64

    how="inner"로 merge했을 때 행이 줄어드는 경우 확인이 어렵다.
    => how="outer", indicator=True로 설정하여 빠진 데이터를 확인할 수 있다.
"""