import pandas as pd
from meteostat import Stations, Daily


#----------- Data Source Management -----------#

#-- SPEED --#

# First datasource from URL: https://offenedaten-koeln.de/sites/default/files/Geschwindigkeit%C3%BCberwachung_Koeln_Gesamt_2017-2021.csv

speed = pd.read_csv('https://offenedaten-koeln.de/sites/default/files/Geschwindigkeit%C3%BCberwachung_Koeln_Gesamt_2017-2021.csv', sep=';', skiprows=1,names=['Jahr ','Monat ','vorfallsdatum','vorfallsuhrzeit','Ortskürzel','geschwindigkeit','ueberschreitung','fahrzeugart','standort','garbage1','garbage2'])


#-- WEATHER --#

# Second datasource from URL: https://meteostat.net/de/place/de/koln?s=D2968&t=2017-01-01/2021-12-31
# We use a designated Python module instead, because there is no online download link

# Alternative: Just use the downloaded data (but that would be too easy of course)
# weather = pd.read_csv('../weather.csv', sep=',')

stations = Stations()
stations = stations.nearby(50.9333, 6.95)  # Cologne coordinates
station = stations.fetch(1)
station_id = station.index[0]

start_date = '2017-01-01'
end_date = '2021-12-31'

weather = Daily(station_id, start=start_date, end=end_date)
weather = weather.fetch()

#----------- Data Manipulation -----------#

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


#-- WEATHER --#

# Add the date column to the DataFrame
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
weather.insert(0, 'date', date_range.strftime('%d-%m-%Y'))

# Deleting all but the date and precipitation columns for the weather data
weather = weather[['date', 'prcp']]
weather['prcp'] = pd.to_numeric(weather['prcp'], errors='coerce')


#----------- Data Export -----------#

# Export to SQL
weather.to_sql('weather', 'sqlite:///../weather.sqlite', if_exists='replace', index=False)
speed.to_sql('speed', 'sqlite:///../speed.sqlite', if_exists='replace', index=False)
