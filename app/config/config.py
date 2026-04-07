import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # schema por defecto
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {
            "options": "-csearch_path=enfermeria_ms"
        }
    }
    
    # Configuración de Auth Service
    AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8085")
    
    # Ambiente (development, production)
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    
    # Configuración de CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    
    # Configuración de seguridad
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET = os.getenv("JWT_SECRET", "8a9b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b")
