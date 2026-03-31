from flask import Blueprint, jsonify, request
from app.models.bitacora_registro import BitacoraRegistro
from app import db
from app.utils.auth import auth_required
from sqlalchemy import func

reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/signos-vitales', methods=['GET'])
@auth_required
def get_signos_vitales():
    paciente_id = request.args.get('paciente_id')
    query = BitacoraRegistro.query
    if paciente_id:
        query = query.filter_by(paciente_id=paciente_id)
    registros = query.all()
    data = [{
        'paciente_id': str(r.paciente_id),
        'fecha': r.cliente_timestamp.isoformat(),
        'signos_vitales': r.signos_vitales
    } for r in registros]
    return jsonify({"mensaje": "Signos vitales obtenidos", "data": data}), 200

@reportes_bp.route('/medicamentos', methods=['GET'])
@auth_required
def get_medicamentos():
    paciente_id = request.args.get('paciente_id')
    query = BitacoraRegistro.query
    if paciente_id:
        query = query.filter_by(paciente_id=paciente_id)
    registros = query.all()
    medicamentos = []
    for r in registros:
        for med in r.medicamentos_administrados:
            medicamentos.append({
                'paciente_id': str(r.paciente_id),
                'fecha': r.cliente_timestamp.isoformat(),
                'medicamento': med
            })
    return jsonify({"mensaje": "Medicamentos obtenidos", "data": medicamentos}), 200

@reportes_bp.route('/turnos', methods=['GET'])
@auth_required
def get_turnos():
    turno = request.args.get('turno')
    query = BitacoraRegistro.query
    if turno:
        query = query.filter_by(turno=turno)
    registros = query.all()
    data = [{
        'id': str(r.id),
        'paciente_id': str(r.paciente_id),
        'turno': r.turno,
        'fecha': r.cliente_timestamp.isoformat(),
        'observaciones': r.observaciones
    } for r in registros]
    return jsonify({"mensaje": "Registros por turno obtenidos", "data": data}), 200