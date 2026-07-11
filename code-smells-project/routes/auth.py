from functools import wraps
from flask import request, jsonify, g
from controllers import usuario_controller

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'erro': 'Token de autorização ausente'}), 401
        
        try:
            if not auth_header.startswith('Bearer '):
                return jsonify({'erro': 'Formato de token inválido'}), 401
            token = auth_header.split(" ")[1]
            if not token.startswith('fake-jwt-token-'):
                return jsonify({'erro': 'Token inválido'}), 401
                
            user_id = int(token.replace('fake-jwt-token-', ''))
            user = usuario_controller.buscar_usuario(user_id)
            g.current_user = user
        except Exception:
            return jsonify({'erro': 'Token inválido ou expirado'}), 401
            
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        user = g.get('current_user')
        if not user or user.get('tipo') != 'admin':
            return jsonify({'erro': 'Acesso restrito para administradores'}), 403
        return f(*args, **kwargs)
    return decorated
