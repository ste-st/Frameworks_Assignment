# Part 1: Data Loading and Basic Exploration

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load metadata.csv
df = pd.read_csv('metadata.csv', low_memory=False)

# Display first 5 rows
print("First 5 rows:")
print(df.head())

# Check DataFrame shape
print("\n DataFrame shape (rows, columns):", df.shape)

# Data types
print("\n Data types:")
print(df.dtypes)

# Check missing values in key columns
print("\nMissing values in important columns:")
important_cols = ['title', 'abstract', 'publish_time', 'journal']
print(df[important_cols].isnull().sum())

# Basic statistics for numerical columns
print("\nBasic statistics for numerical columns:")
print(df.describe())

# Part 2: Data Cleaning & Preparation

# 1️ Handle missing values
missing_percent = df.isnull().mean() * 100
print("\nColumns with many missing values:")
print(missing_percent[missing_percent > 50].sort_values(ascending=False))

# Drop rows missing publication time or title (critical fields)
df_clean = df.dropna(subset=['publish_time', 'title']).copy()

# 2️ Convert date columns to datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Extract year for analysis
df_clean['year'] = df_clean['publish_time'].dt.year

# 3️ Create new column: abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').apply(lambda x: len(x.split()))

print("\nData cleaned and prepared!")
print(df_clean[['title', 'publish_time', 'year', 'abstract_word_count']].head())
# Part 2: Data Cleaning & Preparation

# 1️ Handle missing values
missing_percent = df.isnull().mean() * 100
print("\nColumns with many missing values:")
print(missing_percent[missing_percent > 50].sort_values(ascending=False))

# Drop rows missing publication time or title (critical fields)
df_clean = df.dropna(subset=['publish_time', 'title']).copy()

# 2️ Convert date columns to datetime
df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')

# Extract year for analysis
df_clean['year'] = df_clean['publish_time'].dt.year

# 3️ Create new column: abstract word count
df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').apply(lambda x: len(x.split()))

print("\nData cleaned and prepared!")
print(df_clean[['title', 'publish_time', 'year', 'abstract_word_count']].head())

# Part 3: Data Analysis & Visualization



sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

# 1️ Count papers by year
year_counts = df_clean['year'].value_counts().sort_index()

plt.bar(year_counts.index, year_counts.values, color='skyblue')
plt.title('Number of Publications by Year')
plt.xlabel('Year')
plt.ylabel('Number of Papers')
plt.show()

# 2️ Top journals publishing COVID-19 research
top_journals = df_clean['journal'].value_counts().head(10)

top_journals.plot(kind='bar', color='salmon')
plt.title('Top 10 Journals')
plt.xlabel('Journal')
plt.ylabel('Number of Publications')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 3️ Most frequent words in titles
all_titles = " ".join(df_clean['title'].dropna().astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Paper Titles')
plt.show()

# 4️ Distribution of paper counts by source_x (optional column)
if 'source_x' in df_clean.columns:
    source_counts = df_clean['source_x'].value_counts().head(10)
    source_counts.plot(kind='bar', color='lightgreen')
    plt.title('Top Sources')
    plt.xlabel('Source')
    plt.ylabel('Paper Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

