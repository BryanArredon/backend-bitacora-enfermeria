from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()  # Cargar .env antes de importar Config

from .config.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    # Configuración de CORS basada en variable de entorno
    cors_origins = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    CORS(app, resources={r"/api/*": {"origins": cors_origins}}, supports_credentials=True)

    # Registro de rutas (Blueprints)
    from .routes.pacientes import pacientes_bp
    from .routes.bitacora import bitacora_bp
    from .routes.perfiles import perfiles_bp
    from .routes.auditoria import auditoria_bp
    from .routes.reportes import reportes_bp
    from .routes.cama import camas_bp
    
    app.register_blueprint(pacientes_bp, url_prefix='/api/pacientes')
    app.register_blueprint(bitacora_bp, url_prefix='/api/bitacora')
    app.register_blueprint(perfiles_bp, url_prefix='/api/perfiles')
    app.register_blueprint(auditoria_bp, url_prefix='/api/auditoria')
    app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
    app.register_blueprint(camas_bp, url_prefix='/api/camas')

    # Endpoint de health check (sin autenticación requerida)
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "backend-bitacora-enfermeria",
            "version": "1.0.0",
            "timestamp": "2024-01-01T00:00:00Z"
        }), 200

    return app

# Crear la aplicación cuando se importa el módulo
app = create_app()