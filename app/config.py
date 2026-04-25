import os

class Config:
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    JWT_SECRET = os.getenv("JWT_SECRET", "supersecretkey")