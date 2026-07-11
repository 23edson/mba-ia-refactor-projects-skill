from flask import Blueprint, request, jsonify
from database import get_db
from controllers import pedido_controller
from routes.auth_helper import token_required, admin_required

pedido_bp = Blueprint("pedidos", __name__)

@pedido_bp.route("/pedidos", methods=["POST"])
@token_required
def criar_pedido():
    db = get_db()
    dados = request.get_json()
    resultado = pedido_controller.criar_pedido(db, dados)
    return jsonify({
        "dados": resultado,
        "sucesso": True,
        "mensagem": "Pedido criado com sucesso"
    }), 201

@pedido_bp.route("/pedidos", methods=["GET"])
@token_required
@admin_required
def listar_todos_pedidos():
    db = get_db()
    pedidos = pedido_controller.listar_todos_pedidos(db)
    return jsonify({"dados": pedidos, "sucesso": True}), 200

@pedido_bp.route("/pedidos/usuario/<int:usuario_id>", methods=["GET"])
@token_required
def listar_pedidos_usuario(usuario_id):
    db = get_db()
    pedidos = pedido_controller.listar_pedidos_usuario(db, usuario_id)
    return jsonify({"dados": pedidos, "sucesso": True}), 200

@pedido_bp.route("/pedidos/<int:pedido_id>/status", methods=["PUT"])
@token_required
@admin_required
def atualizar_status_pedido(pedido_id):
    db = get_db()
    dados = request.get_json()
    pedido_controller.atualizar_status_pedido(db, pedido_id, dados)
    return jsonify({"sucesso": True, "mensagem": "Status updated"}), 200
