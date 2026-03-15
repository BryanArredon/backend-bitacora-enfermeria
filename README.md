# 🏥 Bitácora de Enfermería - Backend API (Nursing Service)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)

El backend actúa como el núcleo de procesamiento clínico para el proyecto **"Bitácora de Enfermería"** (UTNG). Su objetivo principal es digitalizar registros hospitalarios y procesar los listados de pacientes y diagnósticos, interactuando de la mano con el `auth-service`.

## ⚙️ Tecnologías y Librerías

* **Python 3.x**
* **Flask** (Framework REST)
* **Flask-SQLAlchemy** (ORM de bases de datos)
* **psycopg** (Driver seguro para PostgreSQL moderno)
* **python-dotenv** (Gestión de secretos)
* **Flask-CORS** (Protección y comunicación multi-origen)

---

## 🔑 Variables de Entorno

El proyecto usa variables de entorno para manejar la cadena de conexión de Supabase de manera segura. Crea un archivo `.env` en base a `.env.example`:

```env
# Ejemplo
SQLALCHEMY_DATABASE_URI="postgresql://postgres:<TU_PASSWORD>@<TU_HOST_SUPABASE>:5432/postgres"
```

---

## 🛠️ Instalación y Ejecución Local

Para levantar este microservicio sin contaminar tus instalaciones globales de Python, sigue este flujo estricto de **entornos virtuales (venv)**:

1. **Crear el entorno virtual** (Solo la primera vez):
   ```bash
   python3 -m venv venv
   ```

2. **Activar el entorno virtual**:
   - En Mac/Linux:
     ```bash
     source venv/bin/activate
     ```
   - En Windows (CMD o PowerShell):
     ```bash
     .\venv\Scripts\activate
     ```

3. **Instalar dependencias** del proyecto:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Ejecutar el Servidor**:
   ```bash
   flask run
   # O alternativamente:
   # python3 -m flask run
   ```

El servicio por defecto arranca en el puerto **5000** (`http://127.0.0.1:5000`).

---

## 🏗️ Estructura del Proyecto

```text
backend-bitacora-enfermeria/
├── app/
│   ├── __init__.py      # Fábrica de la app Flask
│   ├── config/          # Carga de variables del .env
│   ├── models/          # Modelos SQLAlchemy para Tablas Clínicas
│   ├── routes/          # Blueprints (Controladores) de rutas API
│   ├── services/        # Reglas y lógica de procesamiento
│   └── utils/           # Herramientas de formateo o seguridad
├── requirements.txt     # Listado estricto de dependencias
├── app.py               # Punto de entrada de inicialización de DB
└── database/
    └── db.sql           # Esbozos en SQL crudo de las bases de Postgres
```
