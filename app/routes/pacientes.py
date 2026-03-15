from flask import Blueprint, jsonify, request

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/', methods=['GET'])
def get_pacientes():
    return jsonify({"mensaje": "Lista de pacientes obtenida correctamente", "data": []}), 200

@pacientes_bp.route('/', methods=['POST'])
def create_paciente():
    return jsonify({"mensaje": "Paciente creado correctamente"}), 201

@pacientes_bp.route('/<int:id>', methods=['GET'])
def get_paciente(id):
    return jsonify({"mensaje": f"Detalles del paciente {id}"}), 200
