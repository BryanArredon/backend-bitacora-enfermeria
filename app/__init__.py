from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app) 

    # Registro de rutas (Blueprints)
    from .routes.pacientes import pacientes_bp
    from .routes.bitacora import bitacora_bp
    
    app.register_blueprint(pacientes_bp, url_prefix='/api/pacientes')
    app.register_blueprint(bitacora_bp, url_prefix='/api/bitacora')

    return app