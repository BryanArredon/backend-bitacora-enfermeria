from app import db
import uuid
from datetime import datetime

class Paciente(db.Model):
    __tablename__ = "pacientes"
    __table_args__ = {"schema": "enfermeria_ms"}

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_completo = db.Column(db.Text, nullable=False)
    curp = db.Column(db.String(18), unique=True, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.Text, nullable=True)
    fecha_ingreso = db.Column(db.DateTime, default=datetime.utcnow)
    numero_cama = db.Column(db.Text, nullable=True)
    estatus = db.Column(db.Text, default='active')
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
