import pandas as pd


# First datasource from https://offenedaten-koeln.de/sites/default/files/Geschwindigkeit%C3%BCberwachung_Koeln_Gesamt_2017-2021.csv
weather = pd.read_csv('weather.csv', sep=',')

# Second datasource from https://meteostat.net/de/place/de/koln?s=D2968&t=2017-01-01/2021-12-31
speed = pd.read_csv('speed.csv', sep=';', skiprows=1,names=['Jahr ','Monat ','vorfallsdatum','vorfallsuhrzeit','Ortskürzel','geschwindigkeit','ueberschreitung','fahrzeugart','standort','garbage1','garbage2'])

#-- WEATHER --#

# Deleting all but the date and precipitation columns for the weather data
weather = weather[['date', 'prcp']]
weather['date'] = pd.to_datetime(weather['date'])
weather['prcp'] = pd.to_numeric(weather['prcp'], errors='coerce')


#-- SPEED --#

# Formatting of date
speed['vorfallsdatum'] = speed['vorfallsdatum'].astype(str)
valid_indices = speed['vorfallsdatum'].str.match(r'^\d{1,2}\d{4}$').fillna(False)
speed.loc[valid_indices, 'vorfallsdatum'] = speed.loc[valid_indices, 'vorfallsdatum'].str.zfill(6)

# Dataset formatting
speed["date"] = speed["Jahr "].astype(str) + "-" + speed["Monat "].astype(str) + "-" + speed["vorfallsdatum"].astype(str).str[:2]
speed = speed[['date', 'ueberschreitung']]
speed['date'] = pd.to_datetime(speed['date'])
speed['ueberschreitung'] = pd.to_numeric(speed['ueberschreitung'], errors='coerce')

#-- EXPORT --#

# Export to SQL
weather.to_sql('weather', 'sqlite:///weather.sqlite', if_exists='replace', index=False)
speed.to_sql('speed', 'sqlite:///speed.sqlite', if_exists='replace', index=False)

print(speed.tail())