from flask import Blueprint, jsonify, request
from app.models.perfil_enfermeria import PerfilEnfermeria
from app import db
from app.utils.auth import auth_required

perfiles_bp = Blueprint('perfiles', __name__)

@perfiles_bp.route('/', methods=['GET'])
@auth_required
def get_perfiles():
    perfiles = PerfilEnfermeria.query.all()
    data = [{
        'id': str(p.id),
        'nombre_completo': p.nombre_completo,
        'cedula_profesional': p.cedula_profesional,
        'especialidad': p.especialidad,
        'unidad_hospitalaria': p.unidad_hospitalaria,
        'fecha_actualizacion': p.fecha_actualizacion.isoformat()
    } for p in perfiles]
    return jsonify({"mensaje": "Perfiles de enfermería obtenidos", "data": data}), 200

@perfiles_bp.route('/', methods=['POST'])
@auth_required
def create_perfil():
    data = request.get_json()
    nuevo_perfil = PerfilEnfermeria(
        nombre_completo=data['nombre_completo'],
        cedula_profesional=data['cedula_profesional'],
        especialidad=data.get('especialidad'),
        unidad_hospitalaria=data.get('unidad_hospitalaria')
    )
    try:
        db.session.add(nuevo_perfil)
        db.session.commit()
        return jsonify({"mensaje": "Perfil creado", "id": str(nuevo_perfil.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar perfil", "detalle": str(e)}), 500

@perfiles_bp.route('/<uuid:id>', methods=['GET'])
@auth_required
def get_perfil(id):
    perfil = PerfilEnfermeria.query.get_or_404(id)
    data = {
        'id': str(perfil.id),
        'nombre_completo': perfil.nombre_completo,
        'cedula_profesional': perfil.cedula_profesional,
        'especialidad': perfil.especialidad,
        'unidad_hospitalaria': perfil.unidad_hospitalaria,
        'fecha_actualizacion': perfil.fecha_actualizacion.isoformat()
    }
    return jsonify({"mensaje": f"Perfil {id}", "data": data}), 200

@perfiles_bp.route('/<uuid:id>', methods=['PUT'])
@auth_required
def update_perfil(id):
    perfil = PerfilEnfermeria.query.get_or_404(id)
    data = request.get_json()
    perfil.nombre_completo = data.get('nombre_completo', perfil.nombre_completo)
    perfil.cedula_profesional = data.get('cedula_profesional', perfil.cedula_profesional)
    perfil.especialidad = data.get('especialidad', perfil.especialidad)
    perfil.unidad_hospitalaria = data.get('unidad_hospitalaria', perfil.unidad_hospitalaria)
    try:
        db.session.commit()
        return jsonify({"mensaje": "Perfil actualizado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al actualizar perfil", "detalle": str(e)}), 500

@perfiles_bp.route('/<uuid:id>', methods=['DELETE'])
@auth_required
def delete_perfil(id):
    perfil = PerfilEnfermeria.query.get_or_404(id)
    try:
        db.session.delete(perfil)
        db.session.commit()
        return jsonify({"mensaje": "Perfil eliminado"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al eliminar perfil", "detalle": str(e)}), 500