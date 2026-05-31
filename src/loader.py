import pandas as pd

# File path
file_path = "data/Visit_Charges_data.xlsx"

# Read Excel
df = pd.read_excel(file_path)

# Display first 5 rows
print(df.head())

# Dataset information
print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nNull values:")
print(df.isnull().sum().sum())

duplicate_rows = df.duplicated().sum()
print(f"\nDuplicate rows: {duplicate_rows}")

print("\nDataset Info:")
df.info()