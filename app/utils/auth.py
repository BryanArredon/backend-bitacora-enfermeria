import jwt
import os
import requests
from flask import request, jsonify, current_app
from functools import wraps
from urllib.parse import urljoin
import logging

logger = logging.getLogger(__name__)

JWT_SECRET = os.getenv('JWT_SECRET', '8a9b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b')

def get_auth_service_url():
    """Obtiene la URL del auth service según el ambiente"""
    auth_url = os.getenv('AUTH_SERVICE_URL', 'http://localhost:8085')
    return auth_url.rstrip('/')

def verify_token_with_auth_service(token):
    """
    Verifica el token contra el microservicio de autenticación
    
    Retorna:
        dict: Payload del token si es válido
        None: Si el token es inválido
    """
    try:
        auth_service_url = get_auth_service_url()
        
        # Intentar verificar con el auth service
        verify_url = urljoin(auth_service_url, '/api/auth/verify')
        
        response = requests.post(
            verify_url,
            json={'token': token},
            headers={'Content-Type': 'application/json'},
            timeout=5,
            verify=False  # En producción, usar certificados válidos
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.warning(f"Auth service returned status {response.status_code}")
            return None
            
    except requests.RequestException as e:
        logger.warning(f"Could not reach auth service: {str(e)}")
        # Fallback: verificar localmente con JWT
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            return payload
        except jwt.InvalidTokenError:
            return None

def auth_required(fn):
    """
    Decorador que verifica la autenticación del usuario
    
    Puede usar:
    1. Auth service remoto (producción)
    2. JWT local (fallback / desarrollo)
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token requerido"}), 401
        
        token = auth_header.split(' ', 1)[1]
        
        # Intentar verificar con auth service
        payload = verify_token_with_auth_service(token)
        
        if not payload:
            return jsonify({"error": "Token inválido o expirado"}), 401
        
        # Guardar la información del usuario en el request
        request.user = payload
        
        return fn(*args, **kwargs)
    return wrapper

def call_auth_service(endpoint, method='GET', data=None, headers=None):
    """
    Realiza una llamada al microservicio de autenticación
    
    Args:
        endpoint: Endpoint del auth service (ej: '/api/auth/users')
        method: Método HTTP (GET, POST, etc.)
        data: Datos para POST/PUT
        headers: Headers adicionales
        
    Returns:
        Response o None si falla
    """
    try:
        auth_service_url = get_auth_service_url()
        url = urljoin(auth_service_url, endpoint)
        
        default_headers = {
            'Content-Type': 'application/json'
        }
        
        if headers:
            default_headers.update(headers)
        
        if method == 'GET':
            response = requests.get(url, headers=default_headers, timeout=5, verify=False)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=default_headers, timeout=5, verify=False)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=default_headers, timeout=5, verify=False)
        elif method == 'DELETE':
            response = requests.delete(url, headers=default_headers, timeout=5, verify=False)
        else:
            raise ValueError(f"Unsupported method: {method}")
        
        return response
        
    except requests.RequestException as e:
        logger.error(f"Error calling auth service: {str(e)}")
        return None