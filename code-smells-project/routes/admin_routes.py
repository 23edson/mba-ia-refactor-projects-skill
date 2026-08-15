from flask import Blueprint, request, jsonify
from database import get_db
from controllers import admin_controller
from routes.auth_helper import token_required, admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/reset-db", methods=["POST"])
@token_required
@admin_required
def reset_database():
    db = get_db()
    admin_controller.reset_database(db)
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200

@admin_bp.route("/admin/query", methods=["POST"])
@token_required
@admin_required
def executar_query():
    dados = request.get_json()
    query = dados.get("sql", "")
    if not query:
        return jsonify({"erro": "Query não informada"}), 400

    db = get_db()
    try:
        dados_retornados, is_select = admin_controller.executar_query(db, query)
        if is_select:
            return jsonify({"dados": dados_retornados, "sucesso": True}), 200
        else:
            return jsonify({"mensagem": "Query executada", "sucesso": True}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400
