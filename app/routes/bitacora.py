from flask import Blueprint, jsonify, request

bitacora_bp = Blueprint('bitacora', __name__)

@bitacora_bp.route('/', methods=['GET'])
def get_registros():
    return jsonify({"mensaje": "Registros de bitácora obtenidos", "data": []}), 200

@bitacora_bp.route('/', methods=['POST'])
def add_registro():
    return jsonify({"mensaje": "Registro agregado a la bitácora"}), 201
