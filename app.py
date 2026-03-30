from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        print("Creando tablas en la base de datos...")
        db.create_all()
        print("Tablas creadas exitosamente.")
    app.run(debug=True, port=5000)
