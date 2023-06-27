import pandas as pd
from meteostat import Stations, Daily


#----------- Data Source Management -----------#

#-- SPEED --#

### Datasource 1: Speed Monitoring Cologne
# First datasource from URL: https://offenedaten-koeln.de/sites/default/files/Geschwindigkeit%C3%BCberwachung_Koeln_Gesamt_2017-2022_0.csv

# Note: Originally, data from 2017 to 2021 was utilized from the following URL: https://offenedaten-koeln.de/sites/default/files/Geschwindigkeit%C3%BCberwachung_Koeln_Gesamt_2017-2021.csv
# However, this source has been deleted or moved (see ERSTELLT 25.06.2023 at the mobilithek entry). Newly added was the data source for 2017 to 2022, therefore this is used from now on

speed = pd.read_csv('https://offenedaten-koeln.de/sites/default/files/Geschwindigkeit%C3%BCberwachung_Koeln_Gesamt_2017-2022_0.csv', \
    sep=';', skiprows=1, \
        names=['year','month','unformatted_date','incident_time','location_code','speed','excessive_speed','vehicle_type','location','garbage_1','garbage_2'], \
            dtype={0: int, 1: int, 2: int, 3: int, 4: str, 5: str, 6: str, 7: str, 8: str, 9: str, 10: str})


#-- WEATHER --#

### Datasource 2: Weather Review and Climate Data Cologne
# Second datasource from URL: https://meteostat.net/de/place/de/koln?s=D2968&t=2017-01-01/2022-12-31
# We use a designated Python module instead, because there is no online download link

# Alternative: Just use the downloaded data (but that would be boring)
# weather = pd.read_csv('../weather.csv', sep=',')

stations = Stations()
stations = stations.nearby(50.9333, 6.95)  # Cologne coordinates
station = stations.fetch(1)
station_id = station.index[0]

start_date = '2017-01-01'
end_date = '2022-12-31'

weather = Daily(station_id, start=start_date, end=end_date)
weather = weather.fetch()


#----------- Data Manipulation -----------#

#-- SPEED --#

# Formatting of date
speed['unformatted_date'] = speed['unformatted_date'].astype(str)
valid_indices = speed['unformatted_date'].str.match(r'^\d{1,2}\d{4}$').fillna(False)
speed.loc[valid_indices, 'unformatted_date'] = speed.loc[valid_indices, 'unformatted_date'].str.zfill(6)
speed["date"] = speed["year"].astype(str) + "-" + speed["month"].astype(str) + "-" + speed["unformatted_date"].astype(str).str[:2]

# Dataset formatting
speed = speed[['date', 'excessive_speed']]
speed['date'] = pd.to_datetime(speed['date'])
speed['excessive_speed'] = pd.to_numeric(speed['excessive_speed'], errors='coerce')

#-- WEATHER --#

# Add the date column to the DataFrame
date_range = pd.date_range(start=start_date, end=end_date, freq='D')
weather.insert(0, 'date', date_range.strftime('%d-%m-%Y'))

# Dataset formatting
weather = weather[['date', 'prcp']]
weather['date'] = pd.to_datetime(weather['date'], format='%d-%m-%Y')
weather['prcp'] = pd.to_numeric(weather['prcp'], errors='coerce')


#----------- Data Export -----------#

# Export to SQL
weather.to_sql('weather', 'sqlite:///../weather.sqlite', if_exists='replace', index=False)
speed.to_sql('speed', 'sqlite:///../speed.sqlite', if_exists='replace', index=False)
