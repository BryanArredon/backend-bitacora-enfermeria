#!/bin/bash

# Verificar si estamos usando una base de datos externa (Supabase) o local
DB_URI=$(python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv('SQLALCHEMY_DATABASE_URI', ''))
")

if [[ $DB_URI == *"supabase"* ]] || [[ $DB_URI == *"aws-"* ]]; then
    echo "Usando base de datos externa (Supabase). No se requiere espera."
else
    # Esperar a que la base de datos local esté disponible
    echo "Esperando a que la base de datos local esté disponible..."
    while ! nc -z db 5432; do
      sleep 1
    done
    echo "Base de datos local disponible."
fi

# Crear tablas si no existen
echo "Verificando/creando tablas en la base de datos..."
python -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Tablas verificadas/creadas exitosamente.')
"

# Iniciar Gunicorn
echo "Iniciando servidor Gunicorn..."
exec gunicorn \
  --bind 0.0.0.0:8000 \
  --workers 4 \
  --threads 2 \
  --timeout 30 \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  --reload \
  app:app