# 🐍 Hoja de Ruta Maestra: Backend Bitácora (Flask) al 100%

### 🛑 FASE 1: Reparación de Errores Críticos (Urgente)
Antes de programar cosas nuevas, el servidor debe poder arrancar sin romperse y respetar las reglas de internet.
- [ ] **Limpiar Código Basura:** Borrar el decorador huérfano `@bitacora_bp.route('<>')` en el archivo [app/routes/bitacora.py] (Línea 38).
- [ ] **Corregir Verbo HTTP:** Cambiar `methods=['UPDATE']` por `methods=['PUT']` (o `PATCH`) en tu ruta de actualizar registros, ya que `UPDATE` no es un verbo web válido y será bloqueado.
- [ ] **Importar Dependencias Internas faltantes:** Asegurarse de que [Bitacora] y `db` estén correctamente importados al inicio de [bitacora.py] (ej. `from app.models import Bitacora`, `from app import db`), porque actualmente marcan error de no encontrados.

### 🔐 FASE 2: Integración de JWT (La conexión con MS-Seguridad)
Obligar a que Flask valide a los usuarios que inician sesión en Java.
- [ ] **Librería JWT:** Escribir `PyJWT==2.8.0` en el [requirements.txt] e instalarlo (`pip install -r requirements.txt`).
- [ ] **Compartir Clave Maestra:** Declarar `JWT_SECRET` en el archivo [.env] del proyecto con el valor exacto que usas en tu MS de Java.
- [ ] **Crear Guardián Automático:** Crear el archivo [app/utils/security.py] y programar ahí la función `@token_required` que lea el Header `Authorization: Bearer <token>`, lo verifique matemáticamente y rechace (Error 401) si está expirado o fue alterado.
- [ ] **Proteger todas las Rutas:** El equipo debe colocar el `@token_required` debajo de cada petición que manipule datos sensibles de pacientes en sus controladores.

### 🧹 FASE 3: Validación de Datos (Evitar inyecciones o basura)
Actualmente el backend confía ciegamente en cualquier dato que mande el frontend.
- [ ] **Sanitizar el JSON:** Implementar lógica al inicio de las peticiones POST/PUT para verificar que no manden campos vacíos o tipos de datos incorrectos (ej. que la temperatura no venga como la palabra "hola"). Puedes apoyarte de librerías como Marshmallow.
- [ ] **Capturar Errores de Base de Datos:** Los bloques `try-except` están bien, pero deben ser más sofisticados para avisarle al frontend exactamente qué falló (ej. "Paciente no encontrado" vs "Cama ya ocupada").

### 🚀 FASE 4: Rendimiento y Arquitectura Avanzada (Opcional pero Recomendado)
Evita que el sistema colapse cuando tengan millones de registros médicos.
- [ ] **Paginación:** Modificar el endpoint GET `/` (que actualmente trae la lista completa con `.all()`). Si el hospital lleva 30,000 registros, el servidor se quedará sin memoria. Deben devolver los registros en páginas (ej. de 50 en 50).
- [ ] **Auditoría (Quién hizo qué):** Modificar el `@token_required` para que extraiga el correo del enfermero que viene oculto dentro del JWT y guardarlo en la Base de Datos como autor del nuevo registro de signos vitales.
