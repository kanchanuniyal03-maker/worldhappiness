import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("World-happiness-report-2024.csv")

print(df.head())
print(df.describe())

top10 = df.sort_values(by="Ladder score", ascending=False).head(10)

plt.bar(top10["Country name"], top10["Ladder score"])
plt.xticks(rotation=45)
plt.title("Top 10 Happiest Countries")
plt.show()

sns.heatmap(df.corr(numeric_only=True), annot=True)
plt.show()