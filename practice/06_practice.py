"""
    과제 4문제
"""
import matplotlib
# matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from config_06 import setup, out
setup()

# 데이터 로드
df = pd.read_csv('business_data.csv')

# ---------------------------------------------------------------------------------
"""
    [과제 1] 데이터 품질 점검 및 카테고리별 게임 수 및 매출 비교

    [비즈니스 문제 의도]
    : 데이터 분석에 앞서 결측치와 이상치를 파악하고, 
    어느 게임 카테고리에 포트폴리오와 판매량이 집중되어 있는지 
    경영진에게 보고하기 위한 기초 현황을 파악한다.

    [분석 포인트 힌트]
    : isna().sum() 등으로 결측치를 확인하고, 
    seaborn의 countplot 또는 barplot을 활용해 카테고리별 분포를 시각화한다.
"""
# TODO 1: 각 컬럼별 결측치(NaN) 개수를 출력하는 코드를 작성하세요.
print('--- 결측치 현황 ---')
na = df.isnull().sum()
print(na)

# TODO 2: 'category'별 게임 출시 수(Count)를
#          확인할 수 있는 바 차트를 Seaborn으로 그리세요.
fig, ax = plt.subplots(figsize=(8, 5))

sns.countplot(data=df, x="category", ax=ax)

ax.set_title('카테고리별 출시 게임 수 현황')
ax.set_xlabel('게임 카테고리')
ax.set_ylabel('게임 수')
fig.savefig(out("assignment_01.png"), dpi=150)
# plt.show()
plt.close(fig)

# ---------------------------------------------------------------------------------
"""
    [과제 2] 가격(Price)과 판매량(Copies Sold) 간의 상관관계 및 이상치 식별

    [비즈니스 문제 의도]
    : 게임 가격 책정 정책(Pricing Strategy)이 판매량에 미치는 영향을
    파악하고, 전체 트렌드에서 벗어나는 이례적인 타이틀(이상치)을 식별해 
    비즈니스 인사이트를 도출한다.

    [분석 포인트 힌트]
    : sns.scatterplot을 사용하되, hue 파라미터에
    category를 지정하여 카테고리별 군집을 시각화하고
    앞서 발견한 이상치가 어디에 위치하는지 관찰한다.
"""
# TODO 3: price_usd를 X축, copies_sold를 Y축으로 하는 산점도를 그리세요.
# hue에는 'category'를 지정하고, 이상치(Outlier)가 어떻게 시각화되는지 확인합니다.
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

sns.scatterplot(data=df, x="price_usd", y="copies_sold",
                hue="category", s=32, alpha=0.7, ax=axes[0][0])

axes[0][0].set_title('가격(Price) 대비 판매량(Copies Sold) 산점도')
axes[0][0].set_xlabel('가격 (USD)')
axes[0][0].set_ylabel('판매량')

# 로그스케일을 적용한 산점도
sns.scatterplot(data=df, x="price_usd", y="copies_sold",
                hue="category", s=32, alpha=0.7, ax=axes[0][1])

axes[0][1].set_yscale('log')
axes[0][1].set_title('가격 대비 판매량 산점도 (로그스케일 적용)')
axes[0][1].set_xlabel('가격 (USD)')
axes[0][1].set_ylabel('판매량 (Log Scale)')

# 이상치를 제외한 산점도
df_clean = df[(df["copies_sold"] < 10_000_000) & (df["price_usd"] < 100)]

sns.scatterplot(data=df_clean, x="price_usd", y="copies_sold",
                hue="category", s=32, alpha=0.7, ax=axes[1][0])

axes[1][0].set_title('가격 대비 판매량 산점도 (이상치 제외)')
axes[1][0].set_xlabel('가격 (USD)')
axes[1][0].set_ylabel('판매량')

# 축 범위를 지정한 산점도
sns.scatterplot(data=df, x="price_usd", y="copies_sold",
                hue="category", s=32, alpha=0.7, ax=axes[1][1])

axes[1][1].set_xlim(-5, 70)
axes[1][1].set_ylim(-50_000, 1_000_000)
axes[1][1].set_title('가격 대비 판매량 산점도 (축 범위 지정)')
axes[1][1].set_xlabel('가격 (USD)')
axes[1][1].set_ylabel('판매량')

fig.tight_layout()
fig.savefig(out("assignment_02.png"), dpi=150)
plt.show()
plt.close(fig)

# ---------------------------------------------------------------------------------
"""
    [과제 3] 카테고리별 유저 플레이 시간(Playtime)의 분포 및 분산 비교

    [비즈니스 문제 의도]
    : 단순 평균값의 함정에 빠지지 않고, 
    각 게임 카테고리별 유저 몰입도(플레이 시간)의 분포와 편차를 파악하여 
    장르별 유저 락인(Lock-in) 효과를 비교한다.

    [분석 포인트 힌트]
    : sns.boxplot 또는 sns.violinplot을 활용해 
    카테고리별 playtime_hours의 중앙값, 사분위수, 그리고 이상치 분포를 비교한다.
"""
# TODO 4: X축은 'category', Y축은 'playtime_hours'로 하는
#         박스 플롯(Box Plot)을 그리세요.
fig, ax = plt.subplots(figsize=(10, 6))

sns.boxplot(data=df, x="category", y="playtime_hours", ax=ax)
ax.set_title('카테고리별 유저 평균 플레이 시간 분포')
ax.set_xlabel('게임 카테고리')
ax.set_ylabel('플레이 시간 (시간)')
ax.tick_params(axis="x", rotation=15)
fig.savefig(out("assignment_03.png"), dpi=150)
# plt.show()
plt.close(fig)

# ---------------------------------------------------------------------------------
"""
[과제 4] 연도별 및 카테고리별 다차원 매출(판매량) 추이 분석

[비즈니스 문제 의도]
: 시간 흐름(연도)에 따른 카테고리별 성장의 흥망성쇠를 다차원 시각화로 파악하여, 
내년도 투자 포트폴리오 전략 수립에 기여한다.

[분석 포인트 힌트]
: groupby와 pivot_table을 이용해 
연도별-카테고리별 총 판매량 집계 테이블을 만들고, 
sns.heatmap 또는 다중 라인 플롯으로 시각화한다.
"""
# 데이터 집계: 연도 및 카테고리별 총 판매량
pivot_df = df.pivot_table(
    index='category',
    columns='release_year',
    values='copies_sold',
    aggfunc='sum',
)

# TODO 5: 집계된 피벗 테이블을 바탕으로 Seaborn 히트맵(Heatmap)을 그리세요.
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_df, annot=True, fmt=',.0f', cmap='coolwarm')
ax.set_title('연도별/카테고리별 총 판매량 히트맵')
ax.set_xlabel('출시 연도')
ax.set_ylabel('카테고리')
fig.savefig(out("assignment_04.png"), dpi=150)
# plt.show()
plt.close(fig)

