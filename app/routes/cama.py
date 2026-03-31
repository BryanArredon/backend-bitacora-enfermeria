from flask import Blueprint, jsonify, request
from app.models.paciente import Paciente
from app import db
from app.utils.auth import auth_required

camas_bp = Blueprint('camas', __name__)

@camas_bp.route('/', methods=['GET'])
@auth_required
def get_camas():
    pacientes = Paciente.query.filter(Paciente.numero_cama.isnot(None), Paciente.estatus == 'active').all()
    camas = [{
        'numero_cama': p.numero_cama,
        'paciente_id': str(p.id),
        'paciente_nombre': p.nombre_completo
    } for p in pacientes]
    return jsonify({"mensaje": "Camas ocupadas obtenidas", "data": camas}), 200

@camas_bp.route('/disponibles', methods=['GET'])
@auth_required
def get_camas_disponibles():
    # Asumiendo camas del 1 al 20, por ejemplo
    ocupadas = {p.numero_cama for p in Paciente.query.filter(Paciente.numero_cama.isnot(None), Paciente.estatus == 'active').all()}
    total_camas = set(str(i) for i in range(1, 21))  # Ejemplo 1-20
    disponibles = total_camas - ocupadas
    return jsonify({"mensaje": "Camas disponibles", "data": list(disponibles)}), 200