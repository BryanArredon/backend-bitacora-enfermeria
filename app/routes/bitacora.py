from flask import Blueprint, jsonify, request
import requests
import os
from app.models.bitacora_registro import BitacoraRegistro
from app import db
from app.utils.auth import auth_required
from datetime import datetime

bitacora_bp = Blueprint('bitacora', __name__)

AUTH_SERVICE_URL = os.getenv('AUTH_SERVICE_URL', 'http://localhost:8085')

@bitacora_bp.route('/', methods=['GET'])
@auth_required
def get_registros():
    registros = BitacoraRegistro.query.all()
    data = [{
        'id': str(r.id),
        'paciente_id': str(r.paciente_id),
        'enfermero_id': str(r.enfermero_id),
        'turno': r.turno,
        'signos_vitales': r.signos_vitales,
        'observaciones': r.observaciones,
        'medicamentos_administrados': r.medicamentos_administrados,
        'cliente_timestamp': r.cliente_timestamp.isoformat(),
        'es_sincronizado': r.es_sincronizado,
        'fecha_servidor': r.fecha_servidor.isoformat()
    } for r in registros]
    return jsonify({"mensaje": "Registros de bitácora obtenidos", "data": data}), 200

@bitacora_bp.route('/', methods=['POST'])
@auth_required
def add_registro():
    data = request.get_json()
    enfermero_id = request.user['userId']  # Asumiendo que el JWT tiene userId
    nuevo_registro = BitacoraRegistro(
        paciente_id=data['paciente_id'],
        enfermero_id=enfermero_id,
        turno=data['turno'],
        signos_vitales=data.get('signos_vitales', {}),
        observaciones=data['observaciones'],
        medicamentos_administrados=data.get('medicamentos_administrados', []),
        cliente_timestamp=datetime.fromisoformat(data['cliente_timestamp'])
    )
    try:
        db.session.add(nuevo_registro)
        db.session.commit()
        return jsonify({"mensaje": "Registro agregado a la bitácora", "id": str(nuevo_registro.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar registro", "detalle": str(e)}), 500

@bitacora_bp.route('/test-login', methods=['POST'])
def test_login():
    data = request.get_json()
    correo = data.get('correo') or data.get('email')
    password = data.get('password')
    
    if not correo or not password:
        return jsonify({"error": "Correo (o email) y password requeridos"}), 400
    
    try:
        response = requests.post(f"{AUTH_SERVICE_URL}/api/auth/login", json={
            "correo": correo,
            "password": password
        })
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
