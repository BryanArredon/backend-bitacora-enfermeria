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
