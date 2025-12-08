import pandas as pd
import numpy as np

# change the path to your file name
df = pd.read_csv("netflix_titles.csv")

# quick look
print(df.head())
print(df.info())
print(df.isnull().sum())
# example: fill missing text columns with "Unknown"
text_cols_fill_unknown = ["director", "cast", "country", "rating"]
for col in text_cols_fill_unknown:
    df[col] = df[col].fillna("Unknown")

# example: if date_added has nulls, keep them but mark with a flag
df["has_date_added"] = np.where(df["date_added"].isna(), 0, 1)
# drop rows with missing critical columns
df = df.dropna(subset=["title", "type"])
print("Rows before dropping duplicates:", df.shape[0])
df = df.drop_duplicates()
print("Rows after dropping duplicates:", df.shape[0])
# strip spaces and lowercase some columns
df["type"] = df["type"].str.strip().str.lower()          # e.g., "Movie" -> "movie"
df["rating"] = df["rating"].str.strip().str.upper()      # e.g., "tv-ma" -> "TV-MA"
df["country"] = df["country"].fillna("Unknown").str.strip()

# optional: standardize 'type' to exact labels
map_type = {"movie": "Movie", "tv show": "TV Show", "tv show ": "TV Show"}
df["type"] = df["type"].map(map_type).fillna(df["type"])
# convert date_added to datetime with error handling
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

# ensure release_year is integer
df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce").astype("Int64")
# create numeric duration and unit columns
df["duration"] = df["duration"].str.strip()

df["duration_value"] = df["duration"].str.extract(r"(\d+)", expand=False)
df["duration_value"] = pd.to_numeric(df["duration_value"], errors="coerce")

df["duration_unit"] = np.where(df["duration"].str.contains("Season", case=False, na=False),
                               "seasons", "minutes")
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
      .str.replace("-", "_")
)

print(df.columns)
print(df.info())
print(df.isnull().sum())
print(df.head())
df.to_csv("netflix_titles_cleaned.csv", index=False)
