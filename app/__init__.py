
from flask import Flask
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    
    # For development only
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    
    # Import and register blueprints/routes
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app