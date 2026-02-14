from fastapi import APIRouter, HTTPException

from app.services.influx_service import get_latest_weather
from ml.predict import predict_next_30_min

router = APIRouter(prefix="/api/weather", tags=["Weather"])


@router.get("/latest")
def latest_weather():
    """
    Get latest live weather data
    """
    try:
        return get_latest_weather()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predict")
def predict_weather():
    """
    Predict temperature & humidity for next 30 minutes
    """
    try:
        return predict_next_30_min()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
