import numpy as np
import joblib
from datetime import timedelta

from backend.ml.preprocess import preprocess_weather_data


# Load trained models (once)
TEMP_MODEL_PATH = "backend/ml/temp_model.pkl"
HUM_MODEL_PATH = "backend/ml/hum_model.pkl"

temp_model = joblib.load(TEMP_MODEL_PATH)
hum_model = joblib.load(HUM_MODEL_PATH)


def predict_next_30_min():
    """
    Predict temperature & humidity for next 30 minutes
    using latest 60 minutes of data
    """

    # Load clean data
    df = preprocess_weather_data(days=7)

    # Take latest 12 points (last 60 min)
    latest_window = df.tail(12).values  # shape (12, 2)

    if latest_window.shape[0] < 12:
        raise ValueError("Not enough data for prediction")

    # Flatten for linear regression
    X_input = latest_window.reshape(1, -1)  # (1, 24)

    # Predict
    temp_pred = temp_model.predict(X_input)[0]
    hum_pred = hum_model.predict(X_input)[0]

    # Prediction time = last timestamp + 30 minutes
    last_time = df.index[-1]
    prediction_time = last_time + timedelta(minutes=30)

    return {
        "prediction_time": prediction_time.isoformat(),
        "temperature": round(float(temp_pred), 2),
        "humidity": round(float(hum_pred), 2),
    }


if __name__ == "__main__":
    pred = predict_next_30_min()
    print("🔮 Prediction result")
    print(pred)
