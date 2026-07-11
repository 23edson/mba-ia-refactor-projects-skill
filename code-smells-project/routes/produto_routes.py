from flask import Blueprint, request, jsonify
from database import get_db
from controllers import produto_controller
from routes.auth_helper import token_required, admin_required

produto_bp = Blueprint("produtos", __name__)

@produto_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    db = get_db()
    produtos = produto_controller.listar_produtos(db)
    return jsonify({"dados": produtos, "sucesso": True}), 200

@produto_bp.route("/produtos/busca", methods=["GET"])
def buscar_produtos():
    db = get_db()
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria", None)
    preco_min = request.args.get("preco_min", None)
    preco_max = request.args.get("preco_max", None)
    
    resultados = produto_controller.buscar_produtos(db, termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200

@produto_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    db = get_db()
    produto = produto_controller.buscar_produto(db, produto_id)
    return jsonify({"dados": produto, "sucesso": True}), 200

@produto_bp.route("/produtos", methods=["POST"])
@token_required
@admin_required
def criar_produto():
    db = get_db()
    dados = request.get_json()
    resultado = produto_controller.criar_produto(db, dados)
    return jsonify({"dados": resultado, "sucesso": True, "mensagem": "Produto criado"}), 201

@produto_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
@token_required
@admin_required
def atualizar_produto(produto_id):
    db = get_db()
    dados = request.get_json()
    produto_controller.atualizar_produto(db, produto_id, dados)
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

@produto_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
@token_required
@admin_required
def deletar_produto(produto_id):
    db = get_db()
    produto_controller.deletar_produto(db, produto_id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200
