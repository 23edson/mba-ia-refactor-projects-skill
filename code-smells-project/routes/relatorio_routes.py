from flask import Blueprint, jsonify
from controllers import pedido_controller
from routes.auth import admin_required

relatorio_bp = Blueprint("relatorios", __name__)

@relatorio_bp.route("/relatorios/vendas", methods=["GET"])
@admin_required
def relatorio_vendas():
    try:
        relatorio = pedido_controller.relatorio_vendas()
        return jsonify({"dados": relatorio, "sucesso": True}), 200
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500
