"""
    상관 히트맵
"""
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from chart_config import setup, out
from merged_loader import load_merged

setup()
df = load_merged()

# 종목별 일간 수익률(%)
df["ret"] = df.groupby("code")["close"].transform(lambda s: s.pct_change())

# 상관 히트맵: 여러 변수들 간의 상관관계를 계산한 데이터(표)
#              색상의 농도와 밝기로 표현한 그래프
pivot = df.pivot_table(index="date", columns="code", values="ret")
# 긴 형식 (한 행 = 한 종목의 하루) => 넓은 형식 (행 = 날짜, 열 = 종목)
# 섹터 순으로 열을 정렬해야 블록이 제대로 표시됨
order = (df[["code", "sector"]].drop_duplicates()
                               .sort_values(["sector", "code"])["code"]
                               .tolist())
pivot = pivot[order]
# 열 순서를 정렬했으므로, 데이터는 그대로이되 순서만 바뀜

# corr() : 열 간의 상관계수 행렬을 반환
# 종목이 120개이므로 (120, 120) 형태로 반환됨
# [-1, 1] 범위에 있고,
#  -1은 기울기가 음수인 1차함수 꼴, 0은 무관, 1은 기울기가 양수인 1차함수 꼴
corr = pivot.corr()

print(f"pivot: {pivot.shape} (행: 날짜, 열: 종목)")
print(f"corr: {corr.shape} (종목 * 종목 상관계수)")
"""
    pivot: (749, 120) (행: 날짜, 열: 종목)
    corr: (120, 120) (종목 * 종목 상관계수)
"""

fig, ax = plt.subplots(figsize=(9, 7.5))
sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1,
            xticklabels=False, yticklabels=False, ax=ax)
# sns.heatmap(2차원표(상관계수), ...)
# cmap="coolwarm" : 발산형 팔레트. 파랑-회색-빨강 순서로 표시
# center=0: 팔레트 중앙값 지정
# vmin=-1, vmax=1: 색 범위의 양끝을 고정. 미지정 시 데이터의 최소/최대
# xticklabels/yticklabels: 눈금 글자 표시 여부

ax.set_title("종목 간 수익률 상관(섹터순 정렬)")
fig.savefig(out("08_heatmap.png"), dpi=120)
plt.close(fig)

# 설정 없이 그리면 어떻게 되는지 확인
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
# ax는 현재 배열이므로 첫 번째 칸을 가리키도록 axes[0]으로 지정
sns.heatmap(corr, cmap="coolwarm", 
            xticklabels=False, yticklabels=False, ax=axes[0])
axes[0].set_title("center 미지정")

sns.heatmap(corr, cmap="coolwarm", center=0, vmin=-1, vmax=1,
            xticklabels=False, yticklabels=False, ax=axes[1])
axes[1].set_title("center=0, vmin/vmax 설정")

fig.tight_layout()
fig.savefig(out("09_center.png"), dpi=120)
plt.close(fig)

# 섹터 블록을 숫자로 확인
sector_of = df[["code", "sector"]].drop_duplicates().set_index("code")["sector"]
codes = corr.columns        # 상관계수 행렬에서 컬럼이 코드라서

same, diff = [], []
for i in range(len(codes)):
    for j in range(i + 1, len(codes)):
        v = corr.iloc[i, j]

        if sector_of[codes[i]] == sector_of[codes[j]]:
            same.append(v)
        else:
            diff.append(v)

# 상관 행렬은 대칭, 대각선은 항상 1임
# j를 i + 1번째부터 비교하면, 위쪽 삼각형만 순회하게 됨
# => 같은 쌍을 두 번 세거나, 자기 자신과의 비교 자료가 섞이지 않고 추가 가능

print(f"같은 섹터 쌍: {len(same)}개 / 평균: {np.mean(same):.4f}")
print(f"다른 섹터 쌍: {len(diff)}개 / 평균: {np.mean(diff):.4f}")
"""
    수치 상으로 보았을 때, 상관 관계가 섹터별로 존재함
    -> 그래프로는 판단하기 어려움

    시장 전체가 함께 움직이는 요인이 크다보니,
    섹터 차이가 심하게 발생하지는 않기 때문에 바로 식별할 정도가 되지 않음.
"""



