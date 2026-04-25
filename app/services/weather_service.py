import requests
import logging
from flask import current_app

logger = logging.getLogger(__name__)

def get_weather_data(city):
    api_key = current_app.config["WEATHER_API_KEY"]
    base_url = current_app.config["BASE_URL"]
    logger.info(f"API KEY: {api_key}")
    logger.info(f"Fetching weather for city={city}")

    try:
        response = requests.get(
            base_url,
            params={
                "q": city,
                "appid": api_key,
                "units": "metric"
            },
            timeout=5
        )

        logger.info(f"Weather API status={response.status_code}")

        if response.status_code != 200:
            logger.error(f"API failed: {response.text}")
            return None

        data = response.json()

        return {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"]
        }

    except Exception as e:
        logger.exception(f"Exception occurred: {str(e)}")
        return None