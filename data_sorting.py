import pandas as pd

df = pd.read_csv("World-happiness-report-2024.csv")

def get_top10():
    return df.sort_values(by="Ladder score", ascending=False).head(10)

def get_bottom10():
    return df.sort_values(by="Ladder score", ascending=True).head(10)

def get_ranked_data():
    df_copy = df.copy()
    df_copy["Rank"] = df_copy["Ladder score"].rank(ascending=False)
    return df_copy.sort_values("Rank")