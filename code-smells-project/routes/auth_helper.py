from functools import wraps
from flask import request, jsonify, g
from database import get_db
from models import usuario as usuario_model

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'erro': 'Token de autorização ausente'}), 401
        
        try:
            # Padrão: Bearer fake-jwt-token-<id>
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({'erro': 'Formato do token inválido'}), 401
                
            token = parts[1]
            if not token.startswith('fake-jwt-token-'):
                return jsonify({'erro': 'Token inválido'}), 401
                
            usuario_id = int(token.replace('fake-jwt-token-', ''))
            
            db = get_db()
            usuario = usuario_model.get_usuario_por_id(db, usuario_id)
            if not usuario:
                return jsonify({'erro': 'Usuário correspondente ao token não encontrado'}), 401
                
            g.current_user = usuario
        except Exception:
            return jsonify({'erro': 'Token inválido ou corrompido'}), 401
            
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user.get('tipo') != 'admin':
            return jsonify({'erro': 'Acesso negado. Apenas administradores podem acessar esta rota.'}), 403
        return f(*args, **kwargs)
    return decorated
