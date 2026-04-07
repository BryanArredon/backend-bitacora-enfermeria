#!/bin/bash

# Script para probar que la aplicación Flask se puede importar correctamente
# Ejecutar dentro del contenedor o en el directorio del proyecto

echo "🧪 Probando importación de la aplicación Flask..."

cd /app

# Probar importar la aplicación
echo "Probando: python -c 'from app import app; print(\"✅ App importada correctamente\")'"
if python -c "from app import app; print('✅ App importada correctamente')"; then
    echo "✅ La aplicación se importa correctamente"
else
    echo "❌ Error al importar la aplicación"
    exit 1
fi

# Probar que la aplicación tiene las rutas registradas
echo ""
echo "Probando rutas registradas..."
python -c "
from app import app
print('📋 Rutas registradas:')
for rule in app.url_map.iter_rules():
    print(f'  {rule.rule} -> {rule.endpoint}')
"

# Probar que se puede crear la aplicación con create_app()
echo ""
echo "Probando create_app()..."
python -c "
from app import create_app
app = create_app()
print('✅ create_app() funciona correctamente')
print(f'📊 Rutas en create_app(): {len(list(app.url_map.iter_rules()))}')
"

echo ""
echo "🎉 ¡Todas las pruebas pasaron!"