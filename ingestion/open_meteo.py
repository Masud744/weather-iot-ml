import time
import requests
from datetime import datetime, timezone

from influxdb_client import InfluxDBClient, Point, WriteOptions

from app.core.config import (
    INFLUX_URL,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_BUCKET,
)

LATITUDE = 23.97
LONGITUDE = 90.32
INTERVAL = 300  # 5 minutes

API_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&current=temperature_2m,relative_humidity_2m,"
    "pressure_msl,wind_speed_10m,wind_direction_10m"
)

def fetch_weather():
    r = requests.get(
        API_URL.format(lat=LATITUDE, lon=LONGITUDE),
        timeout=10
    )
    r.raise_for_status()
    return r.json()["current"]

def write_to_influx(data):
    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    write_api = client.write_api(
        write_options=WriteOptions(synchronous=True)
    )

    point = (
        Point("weather_live")
        .field("temperature", data["temperature_2m"])
        .field("humidity", data["relative_humidity_2m"])
        .field("pressure", data["pressure_msl"])
        .field("wind_speed", data["wind_speed_10m"])
        .field("wind_direction", data["wind_direction_10m"])
        .time(datetime.now(timezone.utc))
    )

    write_api.write(bucket=INFLUX_BUCKET, record=point)
    client.close()

def run():
    print("🌦 Open-Meteo ingestion worker started")

    while True:
        try:
            data = fetch_weather()
            write_to_influx(data)
            print("✅ Data written at", datetime.now(timezone.utc))
        except Exception as e:
            print("❌ Ingestion error:", e)

        time.sleep(INTERVAL)

if __name__ == "__main__":
    run()
