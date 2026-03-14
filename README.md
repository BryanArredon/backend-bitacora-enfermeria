# 🏥 Bitácora de Enfermería - Backend API (Nursing Service)

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)

[cite_start]Este repositorio contiene el microservicio de **Gestión Clínica** para el proyecto "Plan Estratégico - Bitácora de Enfermería"[cite: 9]. [cite_start]Desarrollado por alumnos de la **Ingeniería en Desarrollo y Gestión de Software** de la **UTNG**[cite: 6, 12].

## 📑 Tabla de Contenidos
1. [Descripción](#-descripción)
2. [Arquitectura](#-arquitectura)
3. [Tecnologías](#-tecnologías)
4. [Instalación](#-instalación)
5. [Endpoints](#-endpoints-api)
6. [Normativa](#-cumplimiento-normativo)

---

## 📖 Descripción
[cite_start]El backend actúa como el núcleo de procesamiento para la digitalización de registros de enfermería[cite: 27]. [cite_start]Su objetivo principal es eliminar la dependencia de formatos físicos, reduciendo errores humanos y garantizando la disponibilidad de la información en tiempo real[cite: 22, 25].

### Características Principales
* [cite_start]**Soporte Offline-First**: Sincronización asíncrona mediante marcas de tiempo de cliente para entornos hospitalarios sin conexión estable[cite: 32, 56].
* **Estructura de Microservicios**: Separación lógica entre identidad (`auth_service`) y operación clínica (`nursing_service`).
* [cite_start]**Seguridad de Grado Médico**: Implementación de Row Level Security (RLS) para proteger datos sensibles de pacientes[cite: 38].

---

## 🏗️ Arquitectura
El sistema utiliza un **API Gateway** que redirige las peticiones a los microservicios correspondientes, cada uno con su propio esquema de base de datos para garantizar el aislamiento y la escalabilidad.



---

## 🛠️ Instalación y Configuración

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install flask flask-cors python-dotenv psycopg2-binary
