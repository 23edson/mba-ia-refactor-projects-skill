from flask import Blueprint, jsonify
from database import get_db
from controllers import relatorio_controller
from routes.auth_helper import token_required, admin_required

relatorio_bp = Blueprint("relatorios", __name__)

@relatorio_bp.route("/relatorios/vendas", methods=["GET"])
@token_required
@admin_required
def relatorio_vendas():
    db = get_db()
    relatorio = relatorio_controller.gerar_relatorio_vendas(db)
    return jsonify({"dados": relatorio, "sucesso": True}), 200
