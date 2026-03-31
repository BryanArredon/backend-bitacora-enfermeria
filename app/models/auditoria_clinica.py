from app import db
import uuid
from datetime import datetime

class AuditoriaClinica(db.Model):
    __tablename__ = "auditoria_clinica"
    __table_args__ = {"schema": "enfermeria_ms"}

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = db.Column(db.UUID(as_uuid=True), nullable=False)
    accion = db.Column(db.Text, nullable=False)
    tabla_afectada = db.Column(db.Text, nullable=False)
    registro_id = db.Column(db.UUID(as_uuid=True), nullable=False)
    datos_anteriores = db.Column(db.JSON, nullable=True)
    datos_nuevos = db.Column(db.JSON, nullable=True)
    fecha_accion = db.Column(db.DateTime, default=datetime.utcnow)