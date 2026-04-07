"""
Servicio para consumir el microservicio de autenticación MS-AUTH
Soporta tanto ambiente local (puerto 8085) como producción (https://ms-auth.bitacoraenfermeria.com)
"""

import requests
import logging
from typing import Optional, Dict, Any
from app.utils.auth import get_auth_service_url, call_auth_service

logger = logging.getLogger(__name__)


class AuthService:
    """Cliente para interactuar con el microservicio de autenticación"""
    
    @staticmethod
    def login(username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Autentica un usuario y obtiene un token JWT
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            
        Returns:
            dict: Con los keys 'token', 'user_id', etc. o None si falla
        """
        response = call_auth_service(
            '/api/auth/login',
            method='POST',
            data={'username': username, 'password': password}
        )
        
        if response and response.status_code == 200:
            return response.json()
        
        logger.error(f"Login failed: {response.status_code if response else 'No response'}")
        return None
    
    @staticmethod
    def register(email: str, password: str, nombre_completo: str, perfil: str = 'enfermera') -> Optional[Dict[str, Any]]:
        """
        Registra un nuevo usuario
        
        Args:
            email: Email del usuario
            password: Contraseña
            nombre_completo: Nombre completo del usuario
            perfil: Perfil del usuario (enfermera, doctor, admin)
            
        Returns:
            dict: Con información del usuario creado o None
        """
        response = call_auth_service(
            '/api/auth/register',
            method='POST',
            data={
                'email': email,
                'password': password,
                'nombre_completo': nombre_completo,
                'perfil': perfil
            }
        )
        
        if response and response.status_code == 201:
            return response.json()
        
        logger.error(f"Registration failed: {response.status_code if response else 'No response'}")
        return None
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verifica que un token JWT sea válido
        
        Args:
            token: Token JWT a verificar
            
        Returns:
            dict: Payload del token si es válido, None si no
        """
        response = call_auth_service(
            '/api/auth/verify',
            method='POST',
            data={'token': token}
        )
        
        if response and response.status_code == 200:
            return response.json()
        
        return None
    
    @staticmethod
    def refresh_token(refresh_token: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un nuevo token usando un refresh token
        
        Args:
            refresh_token: Refresh token del usuario
            
        Returns:
            dict: Con el nuevo token o None
        """
        response = call_auth_service(
            '/api/auth/refresh',
            method='POST',
            data={'refresh_token': refresh_token}
        )
        
        if response and response.status_code == 200:
            return response.json()
        
        return None
    
    @staticmethod
    def get_user_info(user_id: str, token: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene información del usuario
        
        Args:
            user_id: ID del usuario
            token: Token JWT para autorización
            
        Returns:
            dict: Información del usuario o None
        """
        response = call_auth_service(
            f'/api/auth/users/{user_id}',
            method='GET',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response and response.status_code == 200:
            return response.json()
        
        return None
    
    @staticmethod
    def update_user(user_id: str, data: Dict[str, Any], token: str) -> Optional[Dict[str, Any]]:
        """
        Actualiza información del usuario
        
        Args:
            user_id: ID del usuario
            data: Datos a actualizar
            token: Token JWT para autorización
            
        Returns:
            dict: Usuario actualizado o None
        """
        response = call_auth_service(
            f'/api/auth/users/{user_id}',
            method='PUT',
            data=data,
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response and response.status_code == 200:
            return response.json()
        
        return None
    
    @staticmethod
    def list_users(token: str) -> Optional[list]:
        """
        Lista todos los usuarios
        
        Args:
            token: Token JWT para autorización
            
        Returns:
            list: Lista de usuarios o None
        """
        response = call_auth_service(
            '/api/auth/users',
            method='GET',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response and response.status_code == 200:
            return response.json()
        
        return None
    
    @staticmethod
    def delete_user(user_id: str, token: str) -> bool:
        """
        Elimina un usuario
        
        Args:
            user_id: ID del usuario
            token: Token JWT para autorización
            
        Returns:
            bool: True si se eliminó correctamente
        """
        response = call_auth_service(
            f'/api/auth/users/{user_id}',
            method='DELETE',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        return response and response.status_code == 204
    
    @staticmethod
    def get_auth_service_url() -> str:
        """Obtiene la URL del auth service actual"""
        return get_auth_service_url()
    
    @staticmethod
    def health_check() -> bool:
        """Verifica que el auth service esté disponible"""
        response = call_auth_service(
            '/actuator/health',
            method='GET'
        )
        
        return response and response.status_code == 200