import pandas as pd
import urllib.request
import zipfile
from sqlalchemy import create_engine, Integer, Text, Float


#----------- Data Source Management -----------#

url = "https://gtfs.rhoenenergie-bus.de/GTFS.zip"
zip_path = "GTFS.zip"
gtfs_path = "GTFS/"

# Download from URL
urllib.request.urlretrieve(url, zip_path)

# Extract
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(gtfs_path)

# Import dataset
stops_file = gtfs_path + "stops.txt"
df = pd.read_csv(stops_file, sep=',')


#----------- Data Manipulation  -----------#

# Selection
selected_cols = ["stop_id", "stop_name", "stop_lat", "stop_lon", "zone_id"]
df = df[selected_cols]

# Filter zone_id
df = df[df["zone_id"] == 2001]


#----------- Data Cleanup  -----------#

# Drop rows with missing values
df = df.dropna()

# stop_lat and stop_lon
df["stop_lat"] = pd.to_numeric(df["stop_lat"], errors="coerce")
df["stop_lon"] = pd.to_numeric(df["stop_lon"], errors="coerce")
df = df[(df["stop_lat"].between(-90, 90)) & (df["stop_lon"].between(-90, 90))]


#----------- Data Export -----------#

column_types = {
    "stop_id": Integer,
    "stop_name": Text,
    "stop_lat": Float,
    "stop_lon": Float,
    "zone_id": Integer
}

engine = create_engine('sqlite:///gtfs.sqlite')

with engine.begin() as connection:
    df.to_sql("stops", connection, if_exists="replace", index=False, dtype=column_types)
