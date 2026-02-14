import os
import joblib
from datetime import timedelta

from ml.preprocess import preprocess_weather_data

# =========================
# Resolve base directory
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMP_MODEL_PATH = os.path.join(BASE_DIR, "temp_model.pkl")
HUM_MODEL_PATH  = os.path.join(BASE_DIR, "hum_model.pkl")

# Lazy-loaded models
temp_model = None
hum_model = None


def load_models():
    """
    Load ML models only when needed (safe for production)
    """
    global temp_model, hum_model

    if temp_model is None:
        if not os.path.exists(TEMP_MODEL_PATH):
            raise RuntimeError(f"Temperature model not found at {TEMP_MODEL_PATH}")
        temp_model = joblib.load(TEMP_MODEL_PATH)

    if hum_model is None:
        if not os.path.exists(HUM_MODEL_PATH):
            raise RuntimeError(f"Humidity model not found at {HUM_MODEL_PATH}")
        hum_model = joblib.load(HUM_MODEL_PATH)


def predict_next_30_min():
    """
    Predict temperature & humidity for next 30 minutes
    using latest 60 minutes of data
    """

    # Load models safely
    load_models()

    # Load clean data
    df = preprocess_weather_data(days=7)

    # Take latest 12 points (last 60 min)
    latest_window = df.tail(12).values  # (12, 2)

    if latest_window.shape[0] < 12:
        raise ValueError("Not enough data for prediction")

    # Flatten for regression
    X_input = latest_window.reshape(1, -1)  # (1, 24)

    # Predict
    temp_pred = temp_model.predict(X_input)[0]
    hum_pred  = hum_model.predict(X_input)[0]

    # Prediction time
    last_time = df.index[-1]
    prediction_time = last_time + timedelta(minutes=30)

    return {
        "prediction_time": prediction_time.isoformat(),
        "temperature": round(float(temp_pred), 2),
        "humidity": round(float(hum_pred), 2),
    }


if __name__ == "__main__":
    print("🔮 Prediction result")
    print(predict_next_30_min())
