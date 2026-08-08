import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import config
from database import get_db
from routes.auth_helper import token_required, admin_required
from routes.produto_routes import produto_bp
from routes.usuario_routes import usuario_bp
from routes.pedido_routes import pedido_bp
from routes.relatorio_routes import relatorio_bp

# Configura logs do servidor (PT-02 / AP-13)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["DEBUG"] = config.DEBUG
CORS(app)

# Registra os Blueprints (PT-04 / AP-04)
app.register_blueprint(produto_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(relatorio_bp)

@app.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health"
        }
    })

@app.route("/health", methods=["GET"])
def health_check():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        
        cursor.execute("SELECT COUNT(*) FROM produtos")
        produtos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pedidos")
        pedidos = cursor.fetchone()[0]

        return jsonify({
            "status": "ok",
            "database": "connected",
            "counts": {
                "produtos": produtos,
                "usuarios": usuarios,
                "pedidos": pedidos
            },
            "versao": "1.0.0",
            "ambiente": "producao",
            "db_path": config.DATABASE_PATH,
            "debug": config.DEBUG
            # Removido "secret_key" para evitar vazamento de credencial (C-2 / AP-02)
        }), 200
    except Exception:
        return jsonify({"status": "erro", "detalhes": "Não foi possível conectar ao banco de dados"}), 500

@app.route("/admin/reset-db", methods=["POST"])
@token_required
@admin_required
def reset_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()
    
    # Recria o seed do banco de dados (re-insere tabelas e registros padrões)
    from database import init_db
    init_db(db)
    
    logging.warning("!!! BANCO DE DADOS RESETADO PELO ADMINISTRADOR !!!")
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200

@app.route("/admin/query", methods=["POST"])
@token_required
@admin_required
def executar_query():
    dados = request.get_json()
    query = dados.get("sql", "")
    if not query:
        return jsonify({"erro": "Query não informada"}), 400

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            return jsonify({"dados": result, "sucesso": True}), 200
        else:
            db.commit()
            return jsonify({"mensagem": "Query executada", "sucesso": True}), 200
    except Exception as e:
        # Erro amigável para query manual do admin
        return jsonify({"erro": str(e)}), 400

# Centralização de tratamento de erros (PT-08 / AP-10)
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"erro": str(e), "sucesso": False}), 400

@app.errorhandler(Exception)
def handle_generic_error(e):
    logging.error(f"Erro inesperado no servidor: {e}", exc_info=True)
    return jsonify({"erro": "Erro interno do servidor", "sucesso": False}), 500

if __name__ == "__main__":
    # Inicializa banco de dados
    get_db()
    logging.info("==================================================")
    logging.info("SERVIDOR INICIADO")
    logging.info("Rodando em http://localhost:5000")
    logging.info("==================================================")
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
