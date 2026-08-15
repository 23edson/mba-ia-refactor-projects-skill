import jwt
from functools import wraps
from flask import request, jsonify, g
from database import get_db
from models import usuario as usuario_model
from config import SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'erro': 'Token de autorização ausente'}), 401
        
        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({'erro': 'Formato do token inválido'}), 401
                
            token = parts[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            usuario_id = payload.get('sub')
            
            db = get_db()
            usuario = usuario_model.get_usuario_por_id(db, usuario_id)
            if not usuario:
                return jsonify({'erro': 'Usuário correspondente ao token não encontrado'}), 401
                
            g.current_user = usuario
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except (jwt.InvalidTokenError, ValueError):
            return jsonify({'erro': 'Token inválido ou corrompido'}), 401
        except Exception:
            return jsonify({'erro': 'Erro na autenticação'}), 401
            
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user.get('tipo') != 'admin':
            return jsonify({'erro': 'Acesso negado. Apenas administradores podem acessar esta rota.'}), 403
        return f(*args, **kwargs)
    return decorated
