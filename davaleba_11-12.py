import requests
import sqlite3
import json

api_key = "404cd3ec9d668732222cfe228b70b38d"
citi = input("::")
url = f"https://api.openweathermap.org/data/2.5/weather?q={citi}&APPID=404cd3ec9d668732222cfe228b70b38d"

response = requests.get(url)

response_loads = json.loads(response.text)


f = open("weather.json", "w")
json.dump(response_loads, f, indent=4)
f.close()
json_structured = json.dumps(response_loads, indent=4)

ls = [(response_loads["coord"]["lat"],
       response_loads["coord"]["lon"],
       response_loads["name"],
       response_loads["sys"]["country"],
       response_loads["weather"][0]["description"],
       response_loads["wind"]["speed"],
       )]

#
conn = sqlite3.connect("weather_db.sqlite")
cursor = conn.cursor()

# ცხრილში მოცემული იქნება: ქალაქის კოორდინატები(გრძედი და განედი) ქალაქის სახელი, ქვეყნის ინიციალი, ამინდი და ქარის სიჩქარე.

cursor.execute("""CREATE TABLE weather
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude FLOAT,
    longitude FLOAT,
    name VARCHAR(30),
    country VARCHAR(30),
    weather VARCHAR(30),
    wind_speed FLOAT);
""")

cursor.executemany("INSERT INTO weather(latitude, longitude, name, country, weather, wind_speed) VALUES (?,?,?,?,?,?)",
                   ls)
conn.commit()
conn.close()

print(response)
print(response.status_code)
print(response.headers)
print(json_structured)
print(
    f"გრძედი: {ls[0][0]}, განედი: {ls[0][1]}, ქალაქის სახელი: {ls[0][2]}, ქვეყნის ინიციალი: {ls[0][3]}, ამინდი: {ls[0][4]}, ქარის სიჩქარე: {ls[0][5]}")
