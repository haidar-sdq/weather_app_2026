from flask import Flask
from flasgger import Swagger
from app.routes.weather import weather_bp
from app.utils.logger import setup_logger
from app.routes.root import root_bp
from app.routes.auth import auth_bp

def create_app():
    app = Flask(__name__)

    setup_logger()

    app.config.from_object('app.config.Config')

    app.register_blueprint(weather_bp, url_prefix="/api/v1")

    app.register_blueprint(root_bp)
    
    app.register_blueprint(auth_bp)

    Swagger(app)

    return app