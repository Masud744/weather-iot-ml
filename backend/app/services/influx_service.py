from influxdb_client import InfluxDBClient
from backend.app.core.config import (
    INFLUX_URL,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_BUCKET,
)


def get_latest_weather():
    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -1h)
      |> filter(fn: (r) => r._measurement == "weather_live")
      |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> sort(columns: ["_time"], desc: true)
      |> limit(n: 1)
    '''

    tables = client.query_api().query(query)

    client.close()

    if not tables or not tables[0].records:
        return None

    record = tables[0].records[0]

    return {
    "time": record["_time"].isoformat(),
    "temperature": record.values.get("temperature"),
    "humidity": record.values.get("humidity"),
    "pressure": record.values.get("pressure"),
    "wind_speed": record.values.get("wind_speed"),
    "wind_direction": record.values.get("wind_direction"),
   }
