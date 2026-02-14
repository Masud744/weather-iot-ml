from fastapi import APIRouter

from app.services.influx_service import get_latest_weather
from backend.ml.predict import predict_next_30_min

router = APIRouter()

@router.get("/latest")
def latest_weather():
    return get_latest_weather()

@router.get("/predict")
def predict_weather():
    return predict_next_30_min()

