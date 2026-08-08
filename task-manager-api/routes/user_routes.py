import logging
from flask import Blueprint, request, jsonify
from controllers import user_controller
from utils.auth import token_required

logger = logging.getLogger(__name__)
user_bp = Blueprint('users', __name__)

@user_bp.route('/users', methods=['GET'])
@token_required
def get_users():
    try:
        result = user_controller.list_users()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao listar usuários: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao listar usuários'}), 500

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    try:
        data = user_controller.get_user_by_id(user_id)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao buscar usuário {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao buscar usuário'}), 500

@user_bp.route('/users', methods=['POST'])
@token_required
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')

    try:
        user_data = user_controller.create_user(name, email, password, role)
        logger.info(f"Usuário criado: {user_data['id']} - {user_data['name']}")
        return jsonify(user_data), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao criar usuário: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao criar usuário'}), 500

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    try:
        user_data = user_controller.update_user(user_id, data)
        return jsonify(user_data), 200
    except ValueError as e:
        status_code = 404 if "não encontrado" in str(e) else 400
        return jsonify({'error': str(e)}), status_code
    except Exception as e:
        logger.error(f"Erro ao atualizar usuário {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao atualizar usuário'}), 500

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    try:
        user_controller.delete_user(user_id)
        logger.info(f"Usuário deletado: {user_id}")
        return jsonify({'message': 'Usuário deletado com sucesso'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao deletar usuário {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao deletar usuário'}), 500

@user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])
@token_required
def get_user_tasks(user_id):
    try:
        result = user_controller.get_user_tasks(user_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao listar tasks do usuário {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao listar tasks'}), 500

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    email = data.get('email')
    password = data.get('password')

    try:
        login_data = user_controller.login(email, password)
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': login_data['user'],
            'token': login_data['token']
        }), 200
    except ValueError as e:
        err_msg = str(e)
        status_code = 400
        if "Credenciais inválidas" in err_msg:
            status_code = 401
        elif "Usuário inativo" in err_msg:
            status_code = 403
        return jsonify({'error': err_msg}), status_code
    except Exception as e:
        logger.error(f"Erro no login: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno no login'}), 500
