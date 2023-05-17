import pandas as pd

# First datasource from https://offenedaten-koeln.de/sites/default/files/Geschwindigkeit%C3%BCberwachung_Koeln_Gesamt_2017-2021.csv
weather = pd.read_csv('weather.csv', sep=',')

# Second datasource from https://meteostat.net/de/place/de/koln?s=D2968&t=2017-01-01/2021-12-31
speed = pd.read_csv('speed.csv', sep=';', on_bad_lines='skip')

low_memory=False

# Deleting all but the date and precipitation columns for the weather data
for col in weather.columns:
    if col != "date" and col != "prcp":
        weather = weather.drop(columns=[col])
        
# For speed it is unclear for now which data will be relevant, therefore no cleanup just yet


# Export to SQL
weather.to_sql('weather', 'sqlite:///weather.sqlite', if_exists='replace', index=False)
speed.to_sql('speed', 'sqlite:///speed.sqlite', if_exists='replace', index=False)