import pandas as pd
from backend.ml.data_loader import load_weather_data


def preprocess_weather_data(
    days: int = 7,
    interval: str = "5min"
) -> pd.DataFrame:
    """
    Clean & resample weather time-series data for ML
    """

    # Load raw data
    df = load_weather_data(days=days)

    # Convert time column to datetime & set index
    df["time"] = pd.to_datetime(df["time"])
    df = df.set_index("time")

    # Sort by time (safety)
    df = df.sort_index()

    # Resample to fixed interval
    df = df.resample(interval).mean()

    # Handle missing values
    df["temperature"] = df["temperature"].interpolate(method="time")
    df["humidity"] = df["humidity"].interpolate(method="time")

    # Drop any remaining NaNs (edges)
    df = df.dropna()

    return df


if __name__ == "__main__":
    clean_df = preprocess_weather_data(days=7)

    print("✅ Clean ML-ready data")
    print(clean_df.head())
    print("\nShape:", clean_df.shape)
