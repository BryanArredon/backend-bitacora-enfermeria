from app import db
import uuid
from datetime import datetime

class PerfilEnfermeria(db.Model):
    __tablename__ = "perfiles_enfermeria"
    __table_args__ = {"schema": "enfermeria_ms"}

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_completo = db.Column(db.Text, nullable=False)
    cedula_profesional = db.Column(db.Text, unique=True, nullable=False)
    especialidad = db.Column(db.Text, nullable=True)
    unidad_hospitalaria = db.Column(db.Text, nullable=True)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)