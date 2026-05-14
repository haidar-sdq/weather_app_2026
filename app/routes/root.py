from flask import Blueprint

root_bp = Blueprint('root', __name__)

@root_bp.route('/', methods=['GET'])
def home():
    return {
        "message": "Weather API running",
        "version": "v1"
    }, 200

@root_bp.route("/health", methods=["GET"])
def health():
    return {
        "status": "healthy",
        "service": "weather-api"
    }, 200