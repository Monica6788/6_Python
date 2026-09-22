"""
    차트, Seaborn
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from chart_config import setup, out
from merged_loader import load_merged

setup()
df = load_merged()

# 종목별 일간 수익률(%)
df["ret"] = df.groupby("code")["close"].transform(lambda s: s.pct_change() * 100)

"""
    차트 선택 기준 (어떤 용도로 사용할 것인가)

    - 시간에 따른 변화: 선 그래프 (plot)
    - 범주 간 크기 비교: 막대 그래프 (bar)
    - 하나의 분포: 히스토그램 (hist)
    - 분포 + 이상치: 박스플롯 (boxplot)
    - 두 변수의 관계: 산점도 (scatter)
    - 여러 변수의 상관관계: 히트맵 (heatmap)
"""
# 히스토그램 => 분포 확인
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# ax.hist(표시할값들, bins=구간수)
#   값을 bins 개의 구간으로 나누어서 각 구간의 몇 개의 데이터가 있는지 표시
#   hist는 NaN(결측)을 만나면 범위 계산이 깨짐
#   -> dropna()가 선행되어야 함.
axes[0].hist(df["ret"].dropna(), bins=60, color="steelblue", edgecolor="black", linewidth=0.7)
axes[0].set_xlabel("수익률(%)")
axes[0].set_ylabel("빈도")

# 종가 데이터는 NaN 없을 것 같아서 dropna() 생략
axes[1].hist(df["close"], bins=60, color="indianred", edgecolor="black", linewidth=0.7)
axes[1].set_title("종가 분포")
axes[1].set_xlabel("종가(원)")

fig.tight_layout()
fig.savefig(out("04_hist.png"), dpi=120)
plt.close(fig)

print(f"수익률: 평균 {df['ret'].mean():.3f}%, 표준편차 {df['ret'].std():.3f}%")
print(f"종가: 중앙값 {df['close'].median():,.0f}원, 최댓값 {df['close'].max():,.0f}원")
print()

# seaborn으로 boxplot 그리기
# 박스플롯 = IQR 확인하기
# IQR 표기 시 박스의 양 끝이 Q1, Q3가 되고, 수염은 1.5 * IQR 범위가 됨
# 그 외의 점은 이상치로 표현됨.
fig, ax = plt.subplots(figsize=(13, 5))

sns.boxplot(data=df, x="sector", y="ret", ax=ax)
# sns.그래프(data=DataFrame, x="x축이될_열이름", y="y축이될_열이름", ax=Axes)

ax.set_title("섹터별 일간수익률 분포")
ax.set_xlabel("섹터")
ax.set_ylabel("수익률(%)")

# tick_params() : 축에 표시되는 눈금에 대한 설정
ax.tick_params(axis="x", rotation=30)
# x축 눈금에 표시되는 글자를 30º 기울여서 표현

fig.savefig(out("05_box.png"), dpi=120)
plt.close(fig)

q1, q3 = df["ret"].quantile([0.25, 0.75])
iqr = q3 - q1
n_out = ((df["ret"] < q1 - 1.5 * iqr) | (df["ret"] > q3 + 1.5 * iqr)).sum()

print(f"Q1 {q1:.3f} Q3 {q3:3f} IQR {iqr:.3f}")
print(f"범위 내 {q1 - 1.5 * iqr} ~ {q3 + 1.5 * iqr}")
print(f"범위 밖 {n_out:,} 건\n")
# 전체 데이터를 기준으로 이상치를 선별함 -> 의미없는 자료
# 유의미한 자료를 얻기 위해서는 섹터별로 이상치를 선별해야 함.

per_sector = 0

for name, g in  df.groupby("sector"):
    a, b = g["ret"].quantile([0.25, 0.75])
    i = b - a
    per_sector += ((g["ret"] < a - 1.5 * i) | (g["ret"] > b + 1.5 * i)).sum()

print(f"섹터별 실제 이상치 합계: {per_sector:,}건")
print(f"groupby 적용 x - groupby 적용 o = {n_out - per_sector}")

"""
	수익률: 평균 -0.021%, 표준편차 2.615%
	종가: 중앙값 25,040원, 최댓값 579,409원
	
	Q1 -1.353 Q3 1.270834 IQR 2.624
	범위 내 -5.2897743242104145 ~ 5.207199410462829
	범위 밖 2,130 건
	
	섹터별 실제 이상치 합계: 2,028건
	groupby 적용 x - groupby 적용 o = 102
"""

# 산점도
# sample(n, random_state=시드값): 무작위로 n개 행을 추출 (표본추출)
# 시드값은 시작 지점(기준점)
sample = df.dropna(subset=["ret"]).sample(5000, random_state=42)

fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

axes[0].scatter(sample["volume"], sample["ret"], s=1)
# scatter(x, y, s=점크기, alpha=투명도)
# s: 점 하나의 면적. 기본값 36
axes[0].set_title("산점도(기본값)")
axes[0].set_xlabel("거래량")
axes[0].set_ylabel("수익률(%)")

axes[1].scatter(sample["volume"], sample["ret"], s=1, alpha=0.15)
axes[1].set_title("산점도(투명하게)")
axes[1].set_xlabel("거래량")

fig.tight_layout()
fig.savefig(out("06_scatter.png"), dpi=120)
plt.close(fig)


# 막대 그래프 (barplot)

# sns.barplot => 값을 그대로 그리지 않음
# 같은 sector에 속한 데이터의 평균을 막대 하나로 표시함
# 합계를 표시하고자 할 때: estimator="sum" 지정
# 이미 groupby로 집계한 데이터를 넘길 경우 평균의 평균이 될 수 있음.

fig, ax = plt.subplots(figsize=(11, 4))
sns.barplot(data=df, x="sector", y="ret", ax=ax)

ax.axhline(0, color="gray", lw=0.8)
ax.set_title("섹터별 평균 일간수익률")
ax.set_xlabel("섹터")
ax.set_ylabel("평균 수익률(%)")
ax.tick_params(axis="x", rotation=15)

fig.savefig(out("07_bar.png"), dpi=120)
plt.close(fig)

by_sector = df.groupby("sector")["ret"].agg(["mean", "std", "count"])
print(by_sector.round(4))
"""
            mean     std  count
    sector                       
    IT서비스  -0.0212  2.6743  10486
    건설     -0.0311  2.6204   7490
    금융     -0.0093  2.4302  13482
    바이오    -0.0791  2.8107   8988
    식품      0.0013  2.5312   4494
    에너지    -0.0078  2.5417   5992
    운수장비    0.0483  2.6556   8988
    유통     -0.0014  2.5411   8988
    전기전자   -0.0469  2.7240  11984
    화학     -0.0467  2.5722   8988
"""
