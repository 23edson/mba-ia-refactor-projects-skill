from flask import Blueprint, request, jsonify
from controllers import produto_controller

produto_bp = Blueprint("produtos", __name__)

@produto_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    try:
        produtos = produto_controller.listar_produtos()
        return jsonify({"dados": produtos, "sucesso": True}), 200
    except Exception:
        # Centralized logging is done via app handlers, but we can do a simple return here
        # keeping details generic if it's an unexpected error, or specific for domain exceptions
        return jsonify({"erro": "Erro interno no servidor"}), 500

@produto_bp.route("/produtos/busca", methods=["GET"])
def buscar_produtos():
    try:
        termo = request.args.get("q", "")
        categoria = request.args.get("categoria", None)
        preco_min = request.args.get("preco_min", None)
        preco_max = request.args.get("preco_max", None)

        resultados = produto_controller.buscar_produtos(termo, categoria, preco_min, preco_max)
        return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@produto_bp.route("/produtos/<int:produto_id>", methods=["GET"])
def buscar_produto(produto_id):
    try:
        produto = produto_controller.buscar_produto(produto_id)
        return jsonify({"dados": produto, "sucesso": True}), 200
    except KeyError as e:
        return jsonify({"erro": str(e), "sucesso": False}), 404
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@produto_bp.route("/produtos", methods=["POST"])
def criar_produto():
    try:
        dados = request.get_json() or {}
        nome = dados.get("nome")
        descricao = dados.get("descricao", "")
        preco = dados.get("preco")
        estoque = dados.get("estoque")
        categoria = dados.get("categoria", "geral")

        res = produto_controller.criar_produto(nome, descricao, preco, estoque, categoria)
        return jsonify({"dados": res, "sucesso": True, "mensagem": "Produto criado"}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@produto_bp.route("/produtos/<int:produto_id>", methods=["PUT"])
def atualizar_produto(produto_id):
    try:
        dados = request.get_json() or {}
        nome = dados.get("nome")
        descricao = dados.get("descricao", "")
        preco = dados.get("preco")
        estoque = dados.get("estoque")
        categoria = dados.get("categoria", "geral")

        produto_controller.atualizar_produto(produto_id, nome, descricao, preco, estoque, categoria)
        return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except KeyError as e:
        return jsonify({"erro": str(e)}), 404
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500

@produto_bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def deletar_produto(produto_id):
    try:
        produto_controller.deletar_produto(produto_id)
        return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200
    except KeyError as e:
        return jsonify({"erro": str(e)}), 404
    except ValueError as e:
        return jsonify({"erro": str(e)}), 400
    except Exception:
        return jsonify({"erro": "Erro interno no servidor"}), 500
