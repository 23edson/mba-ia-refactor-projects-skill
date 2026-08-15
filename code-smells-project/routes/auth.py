import jwt
from functools import wraps
from flask import request, jsonify, g
from controllers import usuario_controller
from config import SECRET_KEY

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
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('sub')
            
            user = usuario_controller.buscar_usuario(user_id)
            if not user:
                return jsonify({'erro': 'Usuário não encontrado'}), 401
            g.current_user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'erro': 'Token expirado'}), 401
        except (jwt.InvalidTokenError, ValueError):
            return jsonify({'erro': 'Token inválido ou expirado'}), 401
        except Exception:
            return jsonify({'erro': 'Erro na autenticação'}), 401
            
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
