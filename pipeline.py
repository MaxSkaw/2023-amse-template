import pandas as pd

speed = pd.read_csv('speed.csv', sep=';', on_bad_lines='skip')
weather = pd.read_csv('weather.csv', sep=',')

print(weather)
print(speed)

speed

speed.to_sql('speed', 'sqlite:///./data/speed.sqlite', if_exists='replace', index=False)
weather.to_sql('weather', 'sqlite:///./data/weather.sqlite', if_exists='replace', index=False)