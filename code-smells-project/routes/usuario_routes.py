from flask import Blueprint, request, jsonify
from controllers import usuario_controller
from routes.auth import token_required, admin_required

usuario_bp = Blueprint("usuarios", __name__)

@usuario_bp.route("/usuarios", methods=["GET"])
@admin_required
def listar_usuarios():
    try:
        usuarios = usuario_controller.listar_usuarios()
        return jsonify({"dados": usuarios, "sucesso": True}), 200
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@usuario_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
@token_required
def buscar_usuario(usuario_id):
    try:
        usuario = usuario_controller.buscar_usuario(usuario_id)
        return jsonify({"dados": usuario, "sucesso": True}), 200
    except KeyError as e:
        return jsonify({"erro": str(e)}), 404
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@usuario_bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    try:
        dados = request.get_json() or {}
        nome = dados.get("nome")
        email = dados.get("email")
        senha = dados.get("senha")
        
        res = usuario_controller.criar_usuario(nome, email, senha)
        return jsonify({"dados": res, "sucesso": True}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@usuario_bp.route("/login", methods=["POST"])
def login():
    try:
        dados = request.get_json() or {}
        email = dados.get("email", "")
        senha = dados.get("senha", "")
        
        usuario = usuario_controller.login(email, senha)
        return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except PermissionError as e:
        return jsonify({"erro": str(e), "sucesso": False}), 401
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500
