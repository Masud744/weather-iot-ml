from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from config.config import INFLUX_URL, INFLUX_TOKEN, INFLUX_ORG, INFLUX_BUCKET, LOCATION

def write_weather_to_influx(weather):
    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    write_api = client.write_api(write_options=SYNCHRONOUS)

    point = (
        Point("weather_live")
        .tag("location", LOCATION)
        .tag("source", "open_meteo")
        .field("temperature", weather["temperature"])
        .field("humidity", weather["humidity"])
        .field("pressure", weather["pressure"])
        .field("wind_speed", weather["wind_speed"])
        .field("wind_direction", weather["wind_direction"])
    )

    write_api.write(bucket=INFLUX_BUCKET, record=point)
    client.close()
