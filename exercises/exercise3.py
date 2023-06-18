import pandas as pd
from sqlalchemy import create_engine, Integer, Text


#----------- Data Source Management -----------#

# Import dataset
url = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv"
df = pd.read_csv(url, sep=';', encoding="iso-8859-1", engine='python', skiprows=6, skipfooter=4, dtype={"Unnamed: 1": str})


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
final_cols = [df.columns[col_idx] for col_idx in col_nums.keys()]
df = df[final_cols]

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

column_types = {
    "date": Text,
    "CIN": Text,
    "name": Text,
    "petrol": Integer,
    "diesel": Integer,
    "gas": Integer,
    "electro": Integer,
    "hybrid": Integer,
    "plugInHybrid": Integer,
    "others": Integer
}

engine = create_engine('sqlite:///cars.sqlite')

with engine.begin() as connection:
    df.to_sql("cars", connection, if_exists="replace", index=False, dtype=column_types)
