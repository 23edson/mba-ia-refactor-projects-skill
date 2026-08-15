import jwt
from functools import wraps
from flask import request, jsonify, g, current_app
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        
        try:
            parts = auth_header.split()
            if len(parts) != 2 or parts[0].lower() != 'bearer':
                return jsonify({'error': 'Formato do token inválido'}), 401
            
            token = parts[1]
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload.get('sub')
            
            user = User.query.get(user_id)
            if not user or not user.active:
                return jsonify({'error': 'Acesso negado'}), 401
            g.current_user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except (jwt.InvalidTokenError, ValueError):
            return jsonify({'error': 'Token inválido ou expirado'}), 401
        except Exception:
            return jsonify({'error': 'Erro na autenticação'}), 401
            
        return f(*args, **kwargs)
    return decorated

