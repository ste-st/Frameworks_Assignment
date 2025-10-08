# Part 4: Streamlit Application
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load cleaned data
df = pd.read_csv('metadata.csv', low_memory=False)
df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year

st.title("CORD-19 Data Explorer")
st.write("A simple app to explore COVID-19 research metadata.")

# Interactive year range selector
min_year, max_year = int(df['year'].min()), int(df['year'].max())
year_range = st.slider("Select Year Range", min_year, max_year, (2020, 2021))

filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

st.write(f"Showing papers from **{year_range[0]} to {year_range[1]}**. Total: {len(filtered)}")

# Publication count by year
pub_counts = filtered['year'].value_counts().sort_index()

fig, ax = plt.subplots()
ax.bar(pub_counts.index, pub_counts.values, color='skyblue')
ax.set_title('Publications Over Time')
ax.set_xlabel('Year')
ax.set_ylabel('Number of Papers')
st.pyplot(fig)

# Word Cloud of titles
all_titles = " ".join(filtered['title'].dropna().astype(str))
if all_titles.strip():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Sample of the data
st.write("Sample Data")
st.dataframe(filtered[['title', 'journal', 'publish_time']].head(10))
