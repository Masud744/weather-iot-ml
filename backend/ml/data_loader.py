from influxdb_client import InfluxDBClient
import pandas as pd

from app.core.config import (
    INFLUX_URL,
    INFLUX_TOKEN,
    INFLUX_ORG,
    INFLUX_BUCKET,
)


def load_weather_data(days: int = 7, interval: str = "5m") -> pd.DataFrame:
    """
    Load historical weather data from InfluxDB
    :param days: number of past days to fetch
    :param interval: aggregation interval (e.g. 5m)
    :return: Pandas DataFrame
    """

    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    query_api = client.query_api()

    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -{days}d)
      |> filter(fn: (r) => r._measurement == "weather_live")
      |> filter(fn: (r) =>
          r._field == "temperature" or
          r._field == "humidity"
      )
      |> aggregateWindow(every: {interval}, fn: mean, createEmpty: false)
      |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
      |> sort(columns: ["_time"])
    '''

    tables = query_api.query(query)

    records = []
    for table in tables:
        for record in table.records:
            records.append({
                "time": record.get_time(),
                "temperature": record.values.get("temperature"),
                "humidity": record.values.get("humidity"),
            })

    client.close()

    df = pd.DataFrame(records)

    return df


if __name__ == "__main__":
    df = load_weather_data()

    print("✅ Data loaded from InfluxDB")
    print(df.head())
    print("\nShape:", df.shape)

