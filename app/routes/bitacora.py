from flask import Blueprint, jsonify, request, current_app
import os
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import requests
from app.models.bitacora_registro import BitacoraRegistro
from app.models.paciente import Paciente
from app.models.perfil_enfermeria import PerfilEnfermeria

from app import db
from app.utils.auth import auth_required
from app.schemas.bitacora_schema import BitacoraSchema
from marshmallow import ValidationError

bitacora_bp = Blueprint('bitacora', __name__)
schema = BitacoraSchema()


def limpiar_texto(texto):
    return texto.strip()


# =========================
# GET CON PAGINACIÓN
# =========================
@bitacora_bp.route('/', methods=['GET'])
@auth_required
def get_registros():

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    paginacion = BitacoraRegistro.query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

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
    } for r in paginacion.items]

    return jsonify({
        "total": paginacion.total,
        "page": paginacion.page,
        "pages": paginacion.pages,
        "data": data
    }), 200



@bitacora_bp.route('/', methods=['POST'])
@auth_required
def add_registro():

    data = request.get_json()

    if not data:
        return jsonify({"error": "JSON vacío"}), 400

    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify({
            "error": "Datos inválidos",
            "detalles": err.messages
        }), 400

    turno_map = {
        "matutino": "morning",
        "vespertino": "evening",
        "nocturno": "night"
    }

    turno = turno_map.get(validated_data['turno'])

    try:
        # Validar existencia en BD
        paciente = Paciente.query.get(validated_data['paciente_id'])
        if not paciente:
            return jsonify({"error": "Paciente no encontrado"}), 404

        enfermero = PerfilEnfermeria.query.get(validated_data['enfermero_id'])
        if not enfermero:
            return jsonify({"error": "Enfermero no encontrado"}), 404

        nuevo_registro = BitacoraRegistro(
            paciente_id=validated_data['paciente_id'],
            enfermero_id=validated_data['enfermero_id'],
            turno=turno,
            signos_vitales=validated_data.get('signos_vitales', {}),
            observaciones=limpiar_texto(validated_data['observaciones']),
            medicamentos_administrados=validated_data.get('medicamentos_administrados', []),
            cliente_timestamp=datetime.fromisoformat(validated_data['cliente_timestamp']),
            created_by=request.user.get("id")  # 🔐 auditoría
        )

        db.session.add(nuevo_registro)
        db.session.commit()

        return jsonify({
            "mensaje": "Registro agregado correctamente",
            "id": str(nuevo_registro.id)
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Registro duplicado o conflicto en BD"}), 400

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor"}), 500

@bitacora_bp.route('/test-login', methods=['POST'])
def test_login():
    data = request.get_json()
    correo = data.get('correo') or data.get('email')
    password = data.get('password')

    if not correo or not password:
        return jsonify({"error": "Correo (o email) y password requeridos"}), 400

    try:
        response = requests.post(f"{current_app.config['AUTH_SERVICE_URL']}/api/auth/login", json={
            "correo": correo,
            "password": password
        })
        return jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500