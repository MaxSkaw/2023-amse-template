import pandas as pd
from sqlalchemy import create_engine, Integer, Text, Float

engine = create_engine('sqlite:///airports.sqlite')

# Import dataset
df = pd.read_csv('https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv', sep=';', on_bad_lines='skip', low_memory=False)

# Define column types using SQLAlchemy types
column_types = {
    'column_1': Integer,
    'column_2': Text,
    'column_3': Text,
    'column_4': Text,
    'column_5': Integer,
    'column_6': Text,
    'column_7': Float,
    'column_8': Float,
    'column_9': Integer,
    'column_10': Float,
    'column_11': Text,
    'column_12': Text,
    'geo_punkt': Text
}

# Export to SQL
with engine.begin() as connection:
    df.to_sql("airports", connection, if_exists="replace", index=False, dtype=column_types)
