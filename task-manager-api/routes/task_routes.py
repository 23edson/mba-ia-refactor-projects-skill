import logging
from flask import Blueprint, request, jsonify
from controllers import task_controller

logger = logging.getLogger(__name__)
task_bp = Blueprint('tasks', __name__)

@task_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        result = task_controller.list_tasks()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Erro ao listar tasks: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao listar tasks'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        data = task_controller.get_task_by_id(task_id)
        return jsonify(data), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao buscar task {task_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao buscar task'}), 500

@task_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    try:
        task_data = task_controller.create_task(data)
        logger.info(f"Task criada: {task_data['id']} - {task_data['title']}")
        return jsonify(task_data), 201
    except ValueError as e:
        err_msg = str(e)
        status_code = 404 if "não encontrado" in err_msg or "não encontrada" in err_msg else 400
        return jsonify({'error': err_msg}), status_code
    except Exception as e:
        logger.error(f"Erro ao criar task: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao criar task'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    try:
        task_data = task_controller.update_task(task_id, data)
        logger.info(f"Task atualizada: {task_id}")
        return jsonify(task_data), 200
    except ValueError as e:
        err_msg = str(e)
        status_code = 404 if "não encontrada" in err_msg or "não encontrado" in err_msg else 400
        return jsonify({'error': err_msg}), status_code
    except Exception as e:
        logger.error(f"Erro ao atualizar task {task_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao atualizar task'}), 500

@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task_controller.delete_task(task_id)
        logger.info(f"Task deletada: {task_id}")
        return jsonify({'message': 'Task deletada com sucesso'}), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao deletar task {task_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro ao deletar task'}), 500

@task_bp.route('/tasks/search', methods=['GET'])
def search_tasks():
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id = request.args.get('user_id', '')

    try:
        results = task_controller.search_tasks(query, status, priority, user_id)
        return jsonify(results), 200
    except Exception as e:
        logger.error(f"Erro ao pesquisar tasks: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao buscar tasks'}), 500

@task_bp.route('/tasks/stats', methods=['GET'])
def task_stats():
    try:
        stats = task_controller.get_stats()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Erro ao calcular estatísticas: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao calcular estatísticas'}), 500
