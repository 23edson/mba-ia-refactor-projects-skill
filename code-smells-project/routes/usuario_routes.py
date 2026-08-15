from flask import Blueprint, request, jsonify
from database import get_db
from controllers import usuario_controller
from routes.auth_helper import token_required, admin_required

usuario_bp = Blueprint("usuarios", __name__)

@usuario_bp.route("/usuarios", methods=["GET"])
@token_required
@admin_required
def listar_usuarios():
    db = get_db()
    usuarios = usuario_controller.listar_usuarios(db)
    return jsonify({"dados": usuarios, "sucesso": True}), 200

@usuario_bp.route("/usuarios/<int:usuario_id>", methods=["GET"])
@token_required
def buscar_usuario(usuario_id):
    db = get_db()
    usuario = usuario_controller.buscar_usuario(db, usuario_id)
    return jsonify({"dados": usuario, "sucesso": True}), 200

@usuario_bp.route("/usuarios", methods=["POST"])
def criar_usuario():
    db = get_db()
    dados = request.get_json()
    resultado = usuario_controller.criar_usuario(db, dados)
    return jsonify({"dados": resultado, "sucesso": True}), 201

@usuario_bp.route("/login", methods=["POST"])
def login():
    db = get_db()
    dados = request.get_json()
    usuario = usuario_controller.login(db, dados)
    import jwt
    from datetime import datetime, timedelta
    from config import SECRET_KEY
    
    payload = {
        "sub": usuario["id"],
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({
        "dados": usuario,
        "token": token,
        "sucesso": True,
        "mensagem": "Login OK"
    }), 200
