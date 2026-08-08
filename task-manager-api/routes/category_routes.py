import logging
from flask import Blueprint, request, jsonify, g
from utils.auth import token_required
from controllers import category_controller

logger = logging.getLogger(__name__)
category_bp = Blueprint('categories', __name__)

@category_bp.route('/categories', methods=['GET'])
@token_required
def get_categories():
    try:
        result = category_controller.list_categories()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao listar categorias: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao listar categorias'}), 500

@category_bp.route('/categories', methods=['POST'])
@token_required
def create_category():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    name = data.get('name')
    description = data.get('description', '')
    color = data.get('color', '#000000')

    try:
        cat_data = category_controller.create_category(name, description, color)
        return jsonify(cat_data), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Erro ao criar categoria: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao criar categoria'}), 500

@category_bp.route('/categories/<int:cat_id>', methods=['PUT'])
@token_required
def update_category(cat_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    try:
        cat_data = category_controller.update_category(cat_id, data)
        return jsonify(cat_data), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao atualizar categoria {cat_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao atualizar categoria'}), 500

@category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
@token_required
def delete_category(cat_id):
    try:
        category_controller.delete_category(cat_id)
        return jsonify({'message': 'Categoria deletada com sucesso'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao deletar categoria {cat_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao deletar categoria'}), 500
