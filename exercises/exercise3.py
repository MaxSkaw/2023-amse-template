import pandas as pd
import sqlite3


#----------- Data Source Management -----------#

# Import dataset
url = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv"
df = pd.read_csv(url, sep=';', encoding="iso-8859-1", engine='python', skiprows=6, skipfooter=4, dtype={"unnamed: 0": str, "Unnamed: 1": str, "Unnamed: 2": str})


#----------- Data Manipulation  -----------#

col_nums = {
    0: "date",
    1: "CIN",
    2: "name",
    9: "petrol",
    19: "diesel",
    29: "gas",
    42: "electro",
    52: "hybrid",
    62: "plugInHybrid",
    72: "others"
}

# Selection
final_columns = [df.columns[col_idx] for col_idx in col_nums.keys()]
df = df[final_columns]

# Renaming
df.columns = [col_nums[col_idx] for col_idx in col_nums.keys()]


#----------- Data Cleanup  -----------#

# Drop rows with missing values
df = df.dropna()

# CINs
df = df[df["CIN"].str.len() == 5]

# Positive integers
numeric_cols = df.columns.difference(["date", "CIN", "name"])
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
df = df[(df[numeric_cols] > 0).all(axis=1)]


#----------- Data Export -----------#

database = "cars.sqlite"
conn = sqlite3.connect(database)
df.to_sql("cars", conn, if_exists="replace", index=False)
conn.close()
