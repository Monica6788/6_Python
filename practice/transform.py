import pandas as pd

df = pd.DataFrame({ "A": [1, 3, 5, 7], "B": [2, 4, 6, 8], }, index=["r1", "r2", "r3", "r4"])
means = df.groupby("B")["A"].transform("mean")
print(means)
