from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.weather import router as weather_router

app = FastAPI(title="Weather Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(weather_router, prefix="/api/weather", tags=["Weather"])

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Backend is running"
    }
