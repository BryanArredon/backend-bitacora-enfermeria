from flask import Blueprint, jsonify, request
from app.models.paciente import Paciente
from app import db
from app.utils.auth import auth_required

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/', methods=['GET'])
@auth_required
def get_pacientes():
    pacientes = Paciente.query.filter_by(estatus='active').all()
    data = [{
        'id': str(p.id),
        'nombre_completo': p.nombre_completo,
        'curp': p.curp,
        'fecha_nacimiento': p.fecha_nacimiento.isoformat(),
        'genero': p.genero,
        'fecha_ingreso': p.fecha_ingreso.isoformat() if p.fecha_ingreso else None,
        'numero_cama': p.numero_cama,
        'estatus': p.estatus
    } for p in pacientes]
    return jsonify({"mensaje": "Lista de pacientes obtenida correctamente", "data": data}), 200

@pacientes_bp.route('/', methods=['POST'])
@auth_required
def create_paciente():
    data = request.get_json()
    nuevo_paciente = Paciente(
        nombre_completo=data['nombre_completo'],
        curp=data['curp'],
        fecha_nacimiento=data['fecha_nacimiento'],
        genero=data.get('genero'),
        numero_cama=data.get('numero_cama')
    )
    try:
        db.session.add(nuevo_paciente)
        db.session.commit()
        return jsonify({"mensaje": "Paciente creado correctamente", "id": str(nuevo_paciente.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar paciente", "detalle": str(e)}), 500

@pacientes_bp.route('/<uuid:id>', methods=['GET'])
@auth_required
def get_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    data = {
        'id': str(paciente.id),
        'nombre_completo': paciente.nombre_completo,
        'curp': paciente.curp,
        'fecha_nacimiento': paciente.fecha_nacimiento.isoformat(),
        'genero': paciente.genero,
        'fecha_ingreso': paciente.fecha_ingreso.isoformat() if paciente.fecha_ingreso else None,
        'numero_cama': paciente.numero_cama,
        'estatus': paciente.estatus
    }
    return jsonify({"mensaje": f"Detalles del paciente {id}", "data": data}), 200

@pacientes_bp.route('/<uuid:id>', methods=['PUT'])
@auth_required
def update_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    data = request.get_json()
    paciente.nombre_completo = data.get('nombre_completo', paciente.nombre_completo)
    paciente.curp = data.get('curp', paciente.curp)
    paciente.fecha_nacimiento = data.get('fecha_nacimiento', paciente.fecha_nacimiento)
    paciente.genero = data.get('genero', paciente.genero)
    paciente.numero_cama = data.get('numero_cama', paciente.numero_cama)
    paciente.estatus = data.get('estatus', paciente.estatus)
    try:
        db.session.commit()
        return jsonify({"mensaje": "Paciente actualizado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar paciente", "detalle": str(e)}), 500

@pacientes_bp.route('/<uuid:id>', methods=['DELETE'])
@auth_required
def delete_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    paciente.estatus = 'discharged'
    try:
        db.session.commit()
        return jsonify({"mensaje": "Paciente dado de alta correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al dar de alta paciente", "detalle": str(e)}), 500
