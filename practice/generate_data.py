"""
    환경설정 및 실습용 데이터셋 생성 코드
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# --- [한글 폰트 설정] ---
import platform

if platform.system() == 'Windows':
  plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Mac':
  plt.rc('font', family='AppleGothic')
else:
  plt.rc('font', family='DejaVu Sans')
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# --- [가상 데이터셋 생성 (250행)] ---
np.random.seed(42)
n = 250

game_ids = [f'GAME_{i:03d}' for i in range(1, n + 1)]
categories = np.random.choice(
    ['Action', 'RPG', 'Strategy', 'Simulation', 'Indie'],
    size=n,
    p=[0.3, 0.25, 0.15, 0.15, 0.15],
)
release_years = np.random.choice(
    [2021, 2022, 2023, 2024, 2025], size=n, p=[0.1, 0.15, 0.25, 0.3, 0.2]
)
prices = np.random.choice(
    [0.0, 9.99, 19.99, 29.99, 49.99, 59.99], size=n, p=[0.2, 0.2, 0.25, 0.2, 0.1, 0.05]
)
copies_sold = np.random.randint(1000, 800000, size=n)
positive_review_rate = np.random.uniform(0.40, 0.99, size=n)
playtime_hours = np.random.normal(30, 12, size=n).clip(2, 120)

# 현업 데이터 반영: 결측치(NaN) 약 4~6% 주입
mask_nan_1 = np.random.rand(n) < 0.05
positive_review_rate[mask_nan_1] = np.nan
mask_nan_2 = np.random.rand(n) < 0.04
playtime_hours[mask_nan_2] = np.nan

# 현업 데이터 반영: 의심스러운 이상치(Outlier) 주입
copies_sold[12] = 25000000  # 비정상적으로 높은 판매량 (메가 히트 또는 오류)
prices[45] = 299.99  # 비정상적으로 높은 가격

# DataFrame 구성 및 CSV 저장
df = pd.DataFrame({
    'game_id': game_ids,
    'category': categories,
    'release_year': release_years,
    'price_usd': prices,
    'copies_sold': copies_sold,
    'positive_review_rate': positive_review_rate,
    'playtime_hours': playtime_hours,
})

df.to_csv('business_data.csv', index=False)
print(
    f'데이터셋 생성 완료! 총 행 수: {len(df)}, 결측치 현황:\n',
    df.isnull().sum(),
)