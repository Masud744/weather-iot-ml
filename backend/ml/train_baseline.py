import numpy as np
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

from backend.ml.windowing import create_windows
from backend.ml.preprocess import preprocess_weather_data


def train_baseline_model():
    # Load clean data
    df = preprocess_weather_data(days=7)

    # Create windows
    X, y_temp, y_hum = create_windows(df)

    # Flatten input: (samples, 12, 2) → (samples, 24)
    X_flat = X.reshape(X.shape[0], -1)

    # Train-test split
    X_train, X_test, y_temp_train, y_temp_test = train_test_split(
        X_flat, y_temp, test_size=0.2, random_state=42
    )

    _, _, y_hum_train, y_hum_test = train_test_split(
        X_flat, y_hum, test_size=0.2, random_state=42
    )

    # Train models
    temp_model = LinearRegression()
    hum_model = LinearRegression()

    temp_model.fit(X_train, y_temp_train)
    hum_model.fit(X_train, y_hum_train)

    # Predictions
    temp_pred = temp_model.predict(X_test)
    hum_pred = hum_model.predict(X_test)

    # Evaluation
    temp_mae = mean_absolute_error(y_temp_test, temp_pred)
    hum_mae = mean_absolute_error(y_hum_test, hum_pred)

    print("✅ Baseline model trained")
    print(f"Temperature MAE: {temp_mae:.2f} °C")
    print(f"Humidity MAE: {hum_mae:.2f} %")

    # Save models
    joblib.dump(temp_model, "backend/ml/temp_model.pkl")
    joblib.dump(hum_model, "backend/ml/hum_model.pkl")

    print("💾 Models saved to backend/ml/")


if __name__ == "__main__":
    train_baseline_model()
