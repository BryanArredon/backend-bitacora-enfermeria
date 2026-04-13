from app import db
import uuid
from datetime import datetime


class BitacoraRegistro(db.Model):
    __tablename__ = "bitacora_registros"
    __table_args__ = (
        db.UniqueConstraint('paciente_id', 'cliente_timestamp', name='unique_registro'),
        {"schema": "enfermeria_ms"}
    )

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('enfermeria_ms.pacientes.id'), nullable=False)
    enfermero_id = db.Column(db.UUID(as_uuid=True), db.ForeignKey('enfermeria_ms.perfiles_enfermeria.id'), nullable=False)
    turno = db.Column(db.Text, nullable=False)
    signos_vitales = db.Column(db.JSON, default={})
    observaciones = db.Column(db.Text, nullable=False)
    medicamentos_administrados = db.Column(db.JSON, default=[])
    cliente_timestamp = db.Column(db.DateTime, nullable=False)
    es_sincronizado = db.Column(db.Boolean, default=False)
    fecha_servidor = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow)

    paciente = db.relationship('Paciente', backref='bitacora_registros')
    enfermero = db.relationship('PerfilEnfermeria', backref='bitacora_registros')