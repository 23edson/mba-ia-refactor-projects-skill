from flask import Blueprint, request, jsonify, g
from controllers import pedido_controller
from routes.auth import token_required, admin_required

pedido_bp = Blueprint("pedidos", __name__)

@pedido_bp.route("/pedidos", methods=["POST"])
@token_required
def criar_pedido():
    try:
        dados = request.get_json() or {}
        usuario_id = dados.get("usuario_id")
        itens = dados.get("itens", [])
        
        # Validar se o usuário logado coincide com o usuário_id do pedido
        # (a menos que seja admin, mas para simplicidade exigimos consistência)
        current_user = g.get('current_user')
        if current_user and current_user.get('id') != usuario_id and current_user.get('tipo') != 'admin':
            return jsonify({"erro": "Acesso não autorizado para este ID de usuário"}), 403

        resultado = pedido_controller.criar_pedido(usuario_id, itens)
        return jsonify({
            "dados": resultado,
            "sucesso": True,
            "mensagem": "Pedido criado com sucesso"
        }), 201
    except ValueError as e:
        return jsonify({"erro": str(e), "sucesso": False}), 400
    except Exception:
        return jsonify({"erro": "Erro interno no servidor", "sucesso": False}), 500

@pedido_bp.route("/pedidos", methods=["GET"])
@admin_required
def listar_todos_pedidos():
    try:
        pedidos = pedido_controller.listar_todos_pedidos()
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@pedido_bp.route("/pedidos/usuario/<int:usuario_id>", methods=["GET"])
@token_required
def listar_pedidos_usuario(usuario_id):
    try:
        current_user = g.get('current_user')
        if current_user and current_user.get('id') != usuario_id and current_user.get('tipo') != 'admin':
            return jsonify({"erro": "Acesso não autorizado aos pedidos deste usuário"}), 403

        pedidos = pedido_controller.listar_pedidos_usuario(usuario_id)
        return jsonify({"dados": pedidos, "sucesso": True}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@pedido_bp.route("/pedidos/<int:pedido_id>/status", methods=["PUT"])
@admin_required
def atualizar_status_pedido(pedido_id):
    try:
        dados = request.get_json() or {}
        novo_status = dados.get("status", "")
        
        pedido_controller.atualizar_status_pedido(pedido_id, novo_status)
        return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except KeyError as e:
        return jsonify({"erro": str(e)}), 404
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500
