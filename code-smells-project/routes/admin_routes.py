from flask import Blueprint, jsonify
from database import get_db
from routes.auth import admin_required
import logging

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin/reset-db", methods=["POST"])
@admin_required
def reset_database():
    try:
        db = get_db()
        cursor = db.cursor()
        
        # Deletar dados de todas as tabelas para reset
        cursor.execute("DELETE FROM itens_pedido")
        cursor.execute("DELETE FROM pedidos")
        cursor.execute("DELETE FROM produtos")
        cursor.execute("DELETE FROM usuarios")
        db.commit()
        
        logging.warning("BANCO DE DADOS RESETADO POR ADMINISTRADOR")
        return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
    except Exception as e:
        logging.error(f"Erro ao resetar banco de dados: {e}")
        return jsonify({"erro": "Erro interno no servidor"}), 500
