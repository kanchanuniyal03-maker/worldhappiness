import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Happiness Dashboard", layout="wide")

st.title("🌍 World Happiness Report 2024")


df = pd.read_csv("World-happiness-report-2024.csv")


with st.sidebar:
    st.title("Dashboard Controls")

    
    st.subheader("🔍 Search")
    search = st.text_input("Search Country")

    
    st.subheader("Country Filter")
    countries = st.multiselect(
        "Select Countries",
        df["Country name"].unique()
    )

   
    st.subheader("Happiness Score Range")
    min_score, max_score = st.slider(
        "Select Range",
        float(df["Ladder score"].min()),
        float(df["Ladder score"].max()),
        (float(df["Ladder score"].min()), float(df["Ladder score"].max()))
    )

    st.subheader("Select Factor")
    factor = st.selectbox(
        "Choose Factor",
        [
            "Log GDP per capita",
            "Freedom to make life choices",
            "Social support"
        ]
    )

    
    st.subheader("Top N Countries")
    top_n = st.slider("Select number", 5, 20, 10)

    
    st.subheader("Display Options")
    show_heatmap = st.checkbox("Show Heatmap", True)
    show_pie = st.checkbox("Show Pie Chart", True)

    
    st.subheader("Download Data")
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        "happiness_data.csv"
    )


filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Country name"].str.contains(search, case=False)
    ]

if countries:
    filtered_df = filtered_df[
        filtered_df["Country name"].isin(countries)
    ]

filtered_df = filtered_df[
    (filtered_df["Ladder score"] >= min_score) &
    (filtered_df["Ladder score"] <= max_score)
]


st.subheader("Filtered Dataset")
st.write(filtered_df)


st.subheader("Top Happiest Countries")

top_data = filtered_df.sort_values(
    by="Ladder score", ascending=False
).head(top_n)

st.write(top_data[["Country name", "Ladder score"]])

fig1 = px.bar(
    top_data,
    x="Country name",
    y="Ladder score",
    title="Top Countries by Happiness"
)
st.plotly_chart(fig1, use_container_width=True)


st.subheader("Least Happy Countries")

bottom_data = filtered_df.sort_values(
    by="Ladder score", ascending=True
).head(top_n)

st.write(bottom_data[["Country name", "Ladder score"]])


st.subheader("Country Rankings")

ranked_df = filtered_df.copy()
ranked_df["Rank"] = ranked_df["Ladder score"].rank(ascending=False)

st.write(ranked_df.sort_values("Rank")[["Country name", "Rank", "Ladder score"]])


st.subheader("Factor vs Happiness")

fig2 = px.scatter(
    filtered_df,
    x=factor,
    y="Ladder score",
    hover_name="Country name",
    title=f"{factor} vs Happiness"
)
st.plotly_chart(fig2, use_container_width=True)


if show_pie:
    st.subheader("Top 5 Happiness Share")

    top5 = top_data.head(5)

    fig3 = px.pie(
        top5,
        names="Country name",
        values="Ladder score",
        title="Top 5 Countries Share"
    )
    st.plotly_chart(fig3, use_container_width=True)

if show_heatmap:
    st.subheader("Correlation Heatmap")

    fig4, ax = plt.subplots()
    sns.heatmap(filtered_df.corr(numeric_only=True), annot=True, ax=ax)
    st.pyplot(fig4)


st.subheader("🧠 Key Insights")

st.write("""
- Countries with higher GDP tend to be happier  
- Social support strongly impacts happiness  
- Freedom improves life satisfaction  
- Lower score countries often lack economic stability  
""")