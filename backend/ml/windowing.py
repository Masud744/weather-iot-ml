import numpy as np
import pandas as pd

from backend.ml.preprocess import preprocess_weather_data


def create_windows(
    df: pd.DataFrame,
    input_size: int = 12,
    horizon: int = 6
):
    """
    Create sliding windows for ML

    input_size: number of past points (e.g. 12 = last 60 min)
    horizon: how many steps ahead to predict (e.g. 6 = 30 min)
    """

    X = []
    y_temp = []
    y_hum = []

    values = df.values  # shape: (time, features)

    for i in range(len(values) - input_size - horizon + 1):
        # input window
        X.append(values[i : i + input_size])

        # prediction target
        y_temp.append(values[i + input_size + horizon - 1, 0])
        y_hum.append(values[i + input_size + horizon - 1, 1])

    X = np.array(X)
    y_temp = np.array(y_temp)
    y_hum = np.array(y_hum)

    return X, y_temp, y_hum


if __name__ == "__main__":
    df = preprocess_weather_data(days=7)

    X, y_temp, y_hum = create_windows(df)

    print("✅ Windowing complete")
    print("X shape:", X.shape)
    print("y_temp shape:", y_temp.shape)
    print("y_humidity shape:", y_hum.shape)

    print("\nSample input window (first):")
    print(X[0])

    print("\nSample target:")
    print("Temperature:", y_temp[0])
    print("Humidity:", y_hum[0])
