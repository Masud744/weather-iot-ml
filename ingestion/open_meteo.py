import time
import requests
from database.influx import write_weather_to_influx

LATITUDE = 23.97
LONGITUDE = 90.32
INTERVAL = 300  # 5 minutes (300 sec)

while True:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        "&current=temperature_2m,relative_humidity_2m,"
        "pressure_msl,wind_speed_10m,wind_direction_10m"
    )

    response = requests.get(url)
    data = response.json()
    current = data["current"]

    weather_data = {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "pressure": current["pressure_msl"],
        "wind_speed": current["wind_speed_10m"],
        "wind_direction": current["wind_direction_10m"],
        "time": current["time"]
    }

    write_weather_to_influx(weather_data)
    print("✅ Data written:", current["time"])

    time.sleep(INTERVAL)
