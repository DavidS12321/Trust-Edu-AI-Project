from flask import Flask
from dotenv import load_dotenv
import os

def create_app():

    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')

    app = Flask(__name__)
    app.config.from_object('config')

    with app.app_context():
        from .routes import main_bp
        app.register_blueprint(main_bp)

    return app