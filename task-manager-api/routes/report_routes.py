import logging
from flask import Blueprint, jsonify, g
from controllers import report_controller
from utils.auth import token_required

logger = logging.getLogger(__name__)
report_bp = Blueprint('reports', __name__)

@report_bp.route('/reports/summary', methods=['GET'])
@token_required
def summary_report():
    if not g.current_user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    try:
        report = report_controller.get_summary_report()
        return jsonify(report), 200
    except Exception as e:
        logger.error(f"Erro ao gerar relatório geral: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao gerar relatório'}), 500

@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
@token_required
def user_report(user_id):
    if not g.current_user.is_admin():
        return jsonify({'error': 'Acesso negado'}), 403
    try:
        report = report_controller.get_user_report(user_id)
        return jsonify(report), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        logger.error(f"Erro ao gerar relatório do usuário {user_id}: {e}", exc_info=True)
        return jsonify({'error': 'Erro interno ao gerar relatório'}), 500
