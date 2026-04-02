# 🐍 Hoja de Ruta Maestra: Backend Bitácora (Flask) al 100%

### 🚨 FASE 0: Despliegue de Base de Datos (Nuevo - Urgente)
El servidor falla al guardar porque las tablas físicas no existen en Postgres.
- [x] **Crear Tablas en Supabase:** Ejecutar el flujo de creación de tablas (script `db.sql` o ejecutar `python3 app.py` una vez para que SQLAlchemy construya el esquema `enfermeria_ms`).

### 🛑 FASE 1: Reparación de Errores Críticos (Urgente)
Antes de programar cosas nuevas, el servidor debe poder arrancar sin romperse y respetar las reglas de internet.
- [x] **Limpiar Código Basura:** Borrar el decorador huérfano `@bitacora_bp.route('<>')` en el archivo [app/routes/bitacora.py].
- [x] **Corregir Verbo HTTP:** Cambiar `methods=['UPDATE']` por `methods=['PUT']` en tus rutas de actualización.
- [x] **Importar Dependencias Internas faltantes:** Asegurarse de que los Modelos y `db` estén correctamente importados al inicio.

### 🔐 FASE 2: Integración de JWT (La conexión con MS-Seguridad)
Obligar a que Flask valide a los usuarios que inician sesión en Java.
- [x] **Librería JWT:** Escribir `PyJWT` en el [requirements.txt] e instalarlo.
- [x] **Compartir Clave Maestra:** Uso de `JWT_SECRET` compartido (implementado en `app/utils/auth.py`).
- [x] **Crear Guardián Automático:** Crear la función `@auth_required` que lee el Header `Authorization: Bearer <token>` y lo verifica.
- [x] **Proteger todas las Rutas:** `@auth_required` fue colocado exitosamente debajo de cada petición en los controladores.

### 🧹 FASE 3: Validación de Datos (Evitar inyecciones o basura)
Actualmente el backend confía ciegamente en cualquier dato que mande el frontend.
- [X] **Sanitizar el JSON:** Implementar lógica al inicio de las peticiones POST/PUT para verificar que no manden campos vacíos o tipos de datos incorrectos. Apoyarse de `Marshmallow`.
- [X] **Capturar Errores de Base de Datos:** Los bloques `try-except` deben ser más sofisticados para avisarle al frontend exactamente qué falló (ej. "Paciente no encontrado" vs "Cama ya ocupada").

### 🚀 FASE 4: Rendimiento y Arquitectura Avanzada (Opcional pero Recomendado)
Evita que el sistema colapse cuando tengan millones de registros médicos.
- [X] **Paginación:** Modificar el endpoint GET `/` (cambiar `.all()` por paginación). Si el hospital lleva 30,000 registros, el servidor se quedará sin memoria.
- [X] **Auditoría (Quién hizo qué):** Automatizar el registro de auditoría utilizando _Signals_ de SQLAlchemy y extrayendo al autor del token JWT oculto.
- [X] **Capa de Servicios:** Mover las reglas de negocio y cálculos a archivos en `app/services/` para limpiar los crudos controladores de rutas.
