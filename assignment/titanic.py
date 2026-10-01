"""
    20261002_데이터분석_이고은
"""
import os
import numpy as np
import pandas as pd
import platform
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from pathlib import Path
from matplotlib import font_manager

BASE_DIR = Path(__file__).resolve().parent

# round 함수 누락일 경우를 대비하여 옵션 설정
pd.set_option("display.float_format", "{:.2f}".format)

# 시각화 문제를 위한 차트 설정
_DEFAULT_FONT = {
    "Windows": ["Malgun Gothic"],
    "Darwin": ["AppleGothic"]
}
_FALLBACK = ["NanumGothic","Noto Sans CJK KR", "Noto Sans CJK JP", "IPAGothic"]

def find_korean_font():
    """설치된 폰트 중 한글 표시가 가능한 폰트 반환"""
    installed = {f.name for f in font_manager.fontManager.ttflist}

    for name in _DEFAULT_FONT.get(platform.system(), []) + _FALLBACK:
        if name in installed:
            return name
    return None

# 시각화 자료 저장 경로
OUTPUT_DIR = Path(__file__).with_name("output")

def out(name):
    """output/ 내의 파일 경로 반환"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    return OUTPUT_DIR/name

def saved_files():
    """output/ 내부 파일 이름 목록 반환"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    return sorted(p.name for p in OUTPUT_DIR.iterdir() if p.is_file())

def setup(theme=True):
    """한글 폴트 및 마이너스 기호와 seaborn 테마 설정"""
    sns.set_theme(style="whitegrid")
    font = find_korean_font()
    if font:
        plt.rcParams["font.family"] = font
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.dpi"] = 100
    plt.rcParams["savefig.bbox"] = "tight"

setup()

# ============================== 문제 풀이 구간 ==============================
"""
1. pandas를 사용하여 train.csv 파일 데이터를 불러와 DataFrame 으로 저장하시오.
"""
df = pd.read_csv(BASE_DIR / "train.csv", encoding="utf-8-sig")

# ===========================================================================
"""
2. 저장된 데이터에서 상위 5개 행을 출력하시오.
"""
print(df.head())
print()

# ===========================================================================
"""
3. 각 열의 이름, 결측치 여부, 데이터 타입(dtype)을 한 번에 확인하시오.

   df.info()를 실행한 후, 출력 결과를 바탕으로 다음을 기술하시오.    
   - 결측치가 존재하는 열과 결측 개수
   - dtype이 예상과 다르거나 주의가 필요한 열
"""
df.info()
print()

print(f"Age 컬럼 결측: {df['Age'].isnull().sum()}개")         # 177
print(f"Cabin 컬럼 결측: {df['Cabin'].isnull().sum()}개")     # 687
print(f"Embarked 컬럼 결측: {df['Embarked'].isna().sum()}개") # 2
print()

"""
- 결측치가 존재하는 열과 결측 개수
  : Age (177개), Cabin(687개), Embarked(2개)
- dtype이 예상과 다르거나 주의가 필요한 열
  : Age (예상 int64 -> 실제 float64)
"""

# ===========================================================================
"""
4. Age(나이), Fare(요금) 열의 평균값, 최솟값, 최댓값을 구하시오.
"""
age_mean, fare_mean = df["Age"].mean(), df["Fare"].mean()
age_min, fare_min = df["Age"].min(), df["Fare"].min()
age_max, fare_max = df["Age"].max(), df["Fare"].max()
print(f"평균 나이: {age_mean:.2f}세, "
      f"최소 나이: {age_min:.0f}세, "
      f"최대 나이: {age_max:.0f}세")
print(f"평균 요금: {fare_mean:.2f}파운드, "
      f"최소 요금: {fare_min:.0f}파운드, "
      f"최대 요금: {fare_max:.2f}파운드")
print()

# ===========================================================================
"""
5. 탑승객 중 생존자와 사망자가 각각 몇 명인지 계산하시오.

  - 생존자 : Survived=1 / 사망자 : Survived=0
"""
survived = len(df[df["Survived"] == 1])
dead = len(df[df["Survived"] == 0])
print(f"생존자: {survived}명 / 사망자: {dead}명")
print()

# ===========================================================================
"""
6. 객실 등급(Pclass)별로 탑승객이 몇 명인지 계산하시오.
"""
passengers_by_class = df.groupby("Pclass").size()
print(passengers_by_class)
print()

# ===========================================================================
"""
7. 나이가 50세 이상인 탑승객만 추출하여 새로운 데이터프레임을 만드시오.
"""
old = df[df["Age"] >= 50]
print(f"DataFrame old의 최소 나이(결과 확인용): {old['Age'].min()}세")
print()

# ===========================================================================
"""
8. 탑승객을 나이대 기준으로 그룹화하여 새로운 열 AgeGroup을 추가한 후,
   상위 5개 행을 확인하시오.

    나이 범위	AgeGroup 값
    0세 이상 ~ 10세 미만	'아동'
    10세 이상 ~ 20세 미만	'10대'
    20세 이상 ~ 30세 미만	'20대'
    30세 이상 ~ 40세 미만	'30대'
    40세 이상 ~ 50세 미만	'40대'
    50세 이상 ~ 60세 미만	'50대'
    60세 이상	'60대 이상'
    결측치(NaN)	'미확인'
    
  pd.cut() 또는 조건식(if-else / np.where)을 자유롭게 사용해도 됩니다.
"""
# np.where(조건, 참일때값, 거짓일때값) 활용
np_where = df.copy()
np_where["AgeGroup"] = np.where((np_where["Age"] >= 0) & (np_where["Age"] < 10), "아동", 
                 np.where((np_where["Age"] >= 10) & (np_where["Age"] < 20), "10대",  
                 np.where((np_where["Age"] >= 20) & (np_where["Age"] < 30), "20대", 
                 np.where((np_where["Age"] >= 30) & (np_where["Age"] < 40), "30대", 
                 np.where((np_where["Age"] >= 40) & (np_where["Age"] < 50), "40대", 
                 np.where((np_where["Age"] >= 50) & (np_where["Age"] < 60), "50대", 
                 np.where((np_where["Age"] >= 60), "60대 이상", "미확인"
                 )))))))
print(f"np.where() 활용")
print(np_where[['Name', 'Age', 'AgeGroup']].head())
print("-" * 70)

# pd.cut() 활용 (구글링)
pd_cut = df.copy()
ages = pd_cut["Age"].fillna(-1)
boundaries = [-1_000, 0, 10, 20, 30, 40, 50, 60, 1_000]
labels = ["미확인", "아동", "10대", "20대", "30대", "40대", "50대", "60대 이상"]
pd_cut["AgeGroup"] = pd.cut(ages, bins=boundaries, labels=labels, right=False)
print("pd_cut() 활용")
print(pd_cut[['Name', 'Age', 'AgeGroup']].head())
print()

# ===========================================================================
"""
9. 성별(Sex)과 객실 등급(Pclass)을 기준으로 그룹화하여 
   각각의 평균 생존율을 계산하시오.
"""
sex_and_pclass = df.copy().groupby(["Sex", "Pclass"])
survived_rate = round(sex_and_pclass["Survived"].mean(), 2)
survived_rate_pct = round(sex_and_pclass["Survived"].mean() * 100, 2)
print(f"생존률\n{survived_rate}")
print("-" * 40)
print(f"생존률(%)\n{survived_rate_pct}")
print()

# ===========================================================================
"""
10. 나이대별 평균 생존율을 계산하시오.
  - 8번에서 생성한 AgeGroup 열을 기준으로 그룹화하여 계산하시오.
"""
agegroup = np_where.copy().groupby("AgeGroup")
survived_rate = round(agegroup["Survived"].mean(), 2)
survived_rate_pct = round(agegroup["Survived"].mean() * 100, 2)
print(f"생존률\n{survived_rate}")
print()
print(f"생존률(%)\n{survived_rate_pct}")
print()

# ===========================================================================
"""
11. 각 열에 존재하는 결측치(NaN)의 총 개수와
    전체 데이터 대비 비율을 계산하여 내림차순으로 출력하시오.
"""
na_count = df.isna().sum().sort_values(ascending=False)
na_ratio = round(df.isna().mean().sort_values(ascending=False), 2)
na_pct = round(df.isna().mean().sort_values(ascending=False) * 100, 2)
for col in na_count.index:
    if na_count[col] > 0:
        print(f"{col} 컬럼")
        print(f"결측 개수  : {na_count[col]}개")
        print(f"결측률     : {na_ratio[col]}")
        print(f"결측률(%)  : {na_pct[col]}%")
        print("-" * 30)
print()

# ===========================================================================
"""
12. Sex열의 'male'은 0으로, 'female'은 1로 변경하여 
    Gender_Encoded라는 새로운 열을 추가하시오.

  - map(), replace(), apply() 중 편한 방식을 사용해도 됩니다.
"""
# gender_encoded = df.copy()
# gender_encoded["Gender_Encoded"] = np.where(gender_encoded["Sex"] == "male", 0, 1)
# print(gender_encoded[["Gender_Encoded", "Sex"]].head())

# map() 활용
df_map = df.copy()
df_map["Gender_Encoded"] = df_map["Sex"].map({"male": 0, "female": 1})

print("map() 활용")
print(df_map[["Sex", "Gender_Encoded"]].head())
print("-" * 30)

# replace() 활용
df_rep = df.copy()
df_rep["Gender_Encoded"] = df_rep["Sex"]
df_rep = df_rep.replace({"Gender_Encoded": {"male": 0, "female": 1}})
print("replace() 활용")
print(df_rep[["Sex", "Gender_Encoded"]].head())
print("-" * 30)

# .str.replace() 활용
df_str_rep = df.copy()
# male을 먼저 바꾸면 female -> fe0이 되어서 순서 반대로
df_str_rep["Gender_Encoded"] = (df_str_rep["Sex"].str.replace("female", "1")
                                                 .str.replace("male", "0"))
print(".str.replace() 활용")
print(df_str_rep[["Sex", "Gender_Encoded"]].head())
print("-" * 30)

# apply() 활용
df_apply = df.copy()
df_apply['Gender_Encoded'] = (df_apply["Sex"]
                              .apply(lambda x: 0 if x == "male" else 1))
print("apply() 활용")
print(df_apply[["Sex", "Gender_Encoded"]].head())
print()

# ===========================================================================
"""
13. 탑승지(Embarked)별로 승객이 지불한 요금(Fare)의 평균을 계산하시오.
"""
fare_mean_by_embarked = df.copy().groupby("Embarked")
means = round(fare_mean_by_embarked["Fare"].mean(), 2)
print(f"탑승지별 지불 요금 (단위: 파운드)\n{means}")
print()

# ===========================================================================
"""
14. Pclass를 인덱스로, Sex를 컬럼으로, 값으로 Fare의 평균을 사용하여
    피벗 테이블을 생성하시오.
"""
pi = df.copy().pivot_table(
    index="Pclass",
    columns="Sex",
    values="Fare",
    aggfunc="mean"
).round(2)
print(pi)
print()

# ===========================================================================
"""
15. SibSp (형제/배우자 수)와 Parch (부모/자녀 수)를 합산하여
    FamilySize 열을 추가하고, 이 열의 요약 통계를 확인하세요.
"""
family_size = df.copy()
# 본인을 인원수에 포함시키기 위해 +1
family_size["FamilySize"] = family_size["SibSp"] + family_size["Parch"] + 1
print(family_size[["FamilySize"]].describe().round(2))
print()

# ===========================================================================
"""
16. Name 열에서 호칭(Mr., Mrs., Miss., Master. 등)을 정규 표현식 
    또는 문자열 함수를 사용하여 추출하고 Title이라는 새로운 열을 생성한 뒤,
    가장 흔한 5개의 호칭을 출력하시오.

  - 정규 표현식 예시: r', ([A-Za-z]+)\.' - 성(Last name) 뒤에 오는 호칭을 추출한다.
"""
title = df.copy()
title["Title"] = title["Name"].str.extract(r", ([A-Za-z]+)\.")
title_mode = title["Title"].value_counts()
print(title_mode.head())
print()

# ===========================================================================
"""
17. 16번에서 생성한 Title 열을 기준으로 그룹화하여,
    각 호칭별 승객 수, 평균 나이, 평균 생존율을 한 번에 계산하시오.

  - groupby().agg()의 Named Aggregation을 활용하면 
    집계 결과 열 이름을 직접 지정할 수 있다.
"""
summary = title.copy().groupby("Title").agg(
    승객_수=("Name", "count"),
    평균_나이=("Age", "mean"),
    평균_생존율=("Survived", "mean")
).rename(columns={"승객_수":"승객 수", 
                  "평균_나이":"평균 나이", 
                  "평균_생존율": "평균 생존율"}).round(2)
print(summary)
print()

# ===========================================================================
"""
18. 생존한 사람과 사망한 사람의 나이(Age) 분포를 비교할 수 있도록 시각화하시오.

  - 히스토그램 또는 KDE(밀도) 플롯 중 하나를 사용하시오.
  - 그래프에는 다음 요소를 반드시 포함하시오.
    - 제목 (`set_title`)
    - x축·y축 라벨 (`set_xlabel`, `set_ylabel`)
    - 생존/사망 구분 범례 (`legend`)
  - 결과를 화면에 출력하지 않고 이미지 파일로 저장하시오. (`savefig` 사용)
"""
# 히스토그램 (각각)
fig, axes = plt.subplots(1, 2, figsize=(13, 4))

axes[0].hist(df[df["Survived"] == 1]['Age'], bins=8, color="lightgreen", 
             edgecolor="black", linewidth=0.7, label="생존자")
axes[0].set_title("생존자 나이 분포")
axes[0].set_xlabel("나이")
axes[0].set_ylabel("생존자 수")
axes[0].legend()

axes[1].hist(df[df["Survived"] == 0]['Age'], bins=8, color="pink", 
            edgecolor="black", linewidth=0.7, label="사망자")
axes[1].set_title("사망자 나이 분포")
axes[1].set_xlabel("나이")
axes[1].set_ylabel("사망자 수")
axes[1].legend()

fig.tight_layout()
fig.savefig(out("01_hist_seperated.png"), dpi=120)
plt.close(fig)

# 히스토그램 (겹쳐 그리기)
survived = df[df["Survived"] == 1]["Age"]
dead = df[df["Survived"] == 0]["Age"]
bins = np.linspace(df["Age"].min(), df["Age"].max(), 12)

fig, ax = plt.subplots(figsize=(9, 4))

ax.hist(survived, bins=bins, alpha=0.4, edgecolor="gray",
        label="생존자", color="palegreen", linewidth=0.5)
ax.hist(dead, bins=bins, alpha=0.4, edgecolor="gray",
        label="사망자", color="lightpink", linewidth=0.5)
ax.set_title("생존자·사망자 나이 분포")
ax.set_xlabel("나이")
ax.set_ylabel("생존자·사망자 수")
ax.legend()

fig.savefig(out("02_hist_together.png"), dpi=120)
plt.close(fig)

# KDE (pip install scipy 필요)
fig, ax = plt.subplots(figsize=(9, 4))

sns.kdeplot(data=df, x="Age", hue="Survived", fill=True,
            palette=["palegreen", "lightpink"], alpha=0.25)
ax.set_title("생존자·사망자 연령 분포")
ax.set_xlabel("나이")
ax.set_ylabel("밀도")
ax.legend(labels=["사망자", "생존자"])

fig.savefig(out("03_kde.png"), dpi=120)
plt.close(fig)

# ===========================================================================
"""
19. 16번에서 추출한 Title과 Pclass를 동시에 고려하여
    해당 그룹의 나이 중앙값으로 Age 열의 결측치를 대치하시오. 
    (원본 프레임에 적용)
  
  - ex. 'Master' 타이틀을 가진 1등급 승객 그룹의 나이 중앙값으로 
         해당 그룹의 결측치를 채운다.
  - `groupby().transform("median")`을 활용하면 
     그룹별 중앙값을 원본과 같은 길이로 얻을 수 있다.

    ⚠️ 이 문제는 반드시 **16번 완료 후** 진행하시오. 
      `Title` 열이 존재해야 그룹 기준으로 사용할 수 있습니다.
"""
df["Title"] = df["Name"].str.extract(r", ([A-Za-z]+)\.")
df["Age"] = df["Age"].fillna(
    df.groupby(["Title", "Pclass"])["Age"].transform("median")
    )
print(f"대치 후 Age 컬럼 결측: {df['Age'].isnull().sum()}개")

# ===========================================================================
"""
20. Survived, Pclass, Age, SibSp, Parch, Fare 등의 수치형 변수들 간의
    상관관계 행렬을 계산하고, 그 결과를 히트맵(Heatmap) 으로 시각화하시오.

  - `corr()` : 상관관계 행렬 계산 함수
  - `sns.heatmap(..., annot=True, cmap="coolwarm", center=0)` 
     형식으로 작성하면 값이 셀 안에 표시됩니다.
  - 결과를 화면에 출력하지 않고 이미지 파일로 저장하시오. (`savefig` 사용)
"""
NUM_COLS = ["Survived", "Age", "SibSp", "Parch", "Fare"]
pearson = df[NUM_COLS].corr()

fig, ax = plt.subplots(figsize=(10, 10))

sns.heatmap(pearson, cmap="YlGnBu", center=0, vmin=-1, vmax=1,
            xticklabels=NUM_COLS, yticklabels=NUM_COLS, ax=ax, annot=True)
ax.set_title("수치형 변수 간 상관관계 히트맵")

fig.savefig(out("04_heatmap.png"), dpi=120)
plt.close(fig)
# ===========================================================================