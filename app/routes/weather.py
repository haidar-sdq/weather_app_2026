import logging
from flask import Blueprint, jsonify
from app.services.weather_service import get_weather_data
from app.utils.auth_middleware import token_required

logger = logging.getLogger(__name__)

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/weather/<city>', methods=['GET'])
@token_required
def get_weather(city):
    """
    Get weather by city
    ---
    parameters:
      - name: city
        in: path
        type: string
        required: true
    responses:
      200:
        description: Weather data
    """
    
    logger.info(f"Received request for city={city}")

    data = get_weather_data(city)

    if not data:
        logger.warning(f"City not found or API failed for city={city}")
        return jsonify({"error": "City not found"}), 404

    return jsonify(data), 200

@weather_bp.route('/health', methods=['GET'])
def health():
    return {"status": "ok"}, 200