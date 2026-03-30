from flask import Blueprint, jsonify, request
from app.models.auditoria_clinica import AuditoriaClinica
from app import db
from app.utils.auth import auth_required

auditoria_bp = Blueprint('auditoria', __name__)

@auditoria_bp.route('/', methods=['GET'])
@auth_required
def get_auditoria():
    auditorias = AuditoriaClinica.query.all()
    data = [{
        'id': str(a.id),
        'usuario_id': str(a.usuario_id),
        'accion': a.accion,
        'tabla_afectada': a.tabla_afectada,
        'registro_id': str(a.registro_id),
        'datos_anteriores': a.datos_anteriores,
        'datos_nuevos': a.datos_nuevos,
        'fecha_accion': a.fecha_accion.isoformat()
    } for a in auditorias]
    return jsonify({"mensaje": "Auditoría obtenida", "data": data}), 200

@auditoria_bp.route('/', methods=['POST'])
@auth_required
def create_auditoria():
    data = request.get_json()
    nueva_auditoria = AuditoriaClinica(
        usuario_id=data['usuario_id'],
        accion=data['accion'],
        tabla_afectada=data['tabla_afectada'],
        registro_id=data['registro_id'],
        datos_anteriores=data.get('datos_anteriores'),
        datos_nuevos=data.get('datos_nuevos')
    )
    try:
        db.session.add(nueva_auditoria)
        db.session.commit()
        return jsonify({"mensaje": "Auditoría registrada", "id": str(nueva_auditoria.id)}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar auditoría", "detalle": str(e)}), 500