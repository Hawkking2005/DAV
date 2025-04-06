# Step 0: Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Step 1: Load and inspect the dataset
df = pd.read_csv('Finance_data.csv')  # Use the correct file path if different

print("First 5 rows:\n", df.head())
print("\nLast 3 rows:\n", df.tail())
print("\nDataset Info:")
print(df.info())
print("\nMissing Values:\n", df.isna().sum())

# Step 2: Clean the dataset
# Fill missing numeric values with median
for col in df.select_dtypes(include=np.number).columns:
    df[col] = df[col].fillna(df[col].median())

# Fill missing object (categorical) values with mode
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].fillna(df[col].mode()[0])

# Optional: Convert dates if any column is a date
# df['Date'] = pd.to_datetime(df['Date'])

# Step 3: Basic Analysis
print("\nBasic Stats:")
for col in df.select_dtypes(include=np.number).columns:
    print(f"{col} -> Mean: {df[col].mean()}, Median: {df[col].median()}, Std: {df[col].std()}")

# Percentiles
print("\nDescribe numeric columns:\n", df.describe())

# Step 4: Filtering and Sorting
# Example: Filter rows with Profit > 10000
if 'Profit' in df.columns:
    profitable = df[df['Profit'] > 10000]
    print("\nRows with Profit > 10,000:\n", profitable)

# Sorting by Revenue if exists
if 'Revenue' in df.columns:
    sorted_df = df.sort_values(by='Revenue', ascending=False)
    print("\nTop Revenue Rows:\n", sorted_df.head())

# Step 5: Add new column
if 'Revenue' in df.columns and 'Cost' in df.columns:
    df['Net_Profit'] = df['Revenue'] - df['Cost']
    print("\nAdded Net_Profit column.")

# Step 6: Groupby and Pivot Tables
# Groupby example
if 'Category' in df.columns:
    group_stats = df.groupby('Category')['Revenue'].mean()
    print("\nAverage Revenue by Category:\n", group_stats)

# Pivot Table examples
if 'Product' in df.columns and 'Region' in df.columns and 'Revenue' in df.columns:
    pivot1 = pd.pivot_table(df, index='Product', values='Revenue', aggfunc='sum')
    print("\nPivot Table - Revenue by Product:\n", pivot1)

    pivot2 = pd.pivot_table(df, index='Product', columns='Region', values='Revenue', aggfunc='mean')
    print("\nPivot Table - Revenue by Product & Region:\n", pivot2)

# Step 7: Visualizations
# Histogram
numeric_cols = df.select_dtypes(include=np.number).columns
if 'Profit' in numeric_cols:
    plt.figure(figsize=(8, 4))
    plt.hist(df['Profit'], bins=20, color='skyblue')
    plt.title('Profit Distribution')
    plt.xlabel('Profit')
    plt.ylabel('Count')
    plt.show()

# Bar plot
if 'Category' in df.columns and 'Revenue' in df.columns:
    plt.figure(figsize=(8, 4))
    sns.barplot(x='Category', y='Revenue', data=df)
    plt.title('Average Revenue by Category')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Scatter plot
if 'Revenue' in df.columns and 'Cost' in df.columns:
    plt.figure(figsize=(8, 4))
    sns.scatterplot(x='Cost', y='Revenue', data=df)
    plt.title('Revenue vs Cost')
    plt.xlabel('Cost')
    plt.ylabel('Revenue')
    plt.show()

# Box plot
if 'Region' in df.columns and 'Profit' in df.columns:
    plt.figure(figsize=(8, 4))
    sns.boxplot(x='Region', y='Profit', data=df)
    plt.title('Profit Distribution by Region')
    plt.show()

# Step 8: NumPy Advanced (Z-score normalization)
if 'Profit' in df.columns:
    profit_mean = np.mean(df['Profit'])
    profit_std = np.std(df['Profit'])
    df['Profit_zscore'] = (df['Profit'] - profit_mean) / profit_std
    print("\nProfit column normalized (z-score).")
