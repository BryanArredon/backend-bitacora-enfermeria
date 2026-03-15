from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config
from app import create_app

db = SQLAlchemy()

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
