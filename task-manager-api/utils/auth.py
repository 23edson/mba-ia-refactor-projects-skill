from functools import wraps
from flask import request, jsonify, g
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        
        try:
            # Para o mock/fake-jwt utilizado neste projeto
            user_id = int(token.replace('Bearer fake-jwt-token-', ''))
            user = User.query.get(user_id)
            if not user or not user.active:
                return jsonify({'error': 'Acesso negado'}), 401
            g.current_user = user
        except Exception:
            return jsonify({'error': 'Token inválido'}), 401
        return f(*args, **kwargs)
    return decorated
