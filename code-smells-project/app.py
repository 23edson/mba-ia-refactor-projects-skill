from flask import Flask, jsonify
from flask_cors import CORS
import config
from database import get_db
import logging

# Import Blueprints
from routes.produto_routes import produto_bp
from routes.usuario_routes import usuario_bp
from routes.pedido_routes import pedido_bp
from routes.relatorio_routes import relatorio_bp
from routes.admin_routes import admin_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["DEBUG"] = config.DEBUG
CORS(app)

# Register Blueprints
app.register_blueprint(produto_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(pedido_bp)
app.register_blueprint(relatorio_bp)
app.register_blueprint(admin_bp)

# Health check route
@app.route("/health", methods=["GET"])
def health_check():
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        
        cursor.execute("SELECT COUNT(*) FROM produtos WHERE ativo = 1")
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
            "ambiente": "desenvolvimento" if config.DEBUG else "producao"
            # Omitida a chave secreta aqui para evitar vazamento de credenciais (AP-02)
        }), 200
    except Exception as e:
        logging.error(f"Erro no health check: {e}")
        return jsonify({"status": "erro", "detalhes": "Não foi possível conectar ao banco de dados"}), 500

# Home route (welcome message)
@app.route("/", methods=["GET"])
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

# Centralized Error Handlers (PT-08)
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"erro": str(e)}), 400

@app.errorhandler(KeyError)
def handle_key_error(e):
    msg = str(e).strip("'").strip('"')
    return jsonify({"erro": msg}), 404

@app.errorhandler(PermissionError)
def handle_permission_error(e):
    return jsonify({"erro": str(e)}), 401

@app.errorhandler(Exception)
def handle_generic_error(e):
    logging.error(f"Erro inesperado: {e}", exc_info=True)
    return jsonify({"erro": "Erro interno no servidor"}), 500

if __name__ == "__main__":
    # Inicia e popula banco se necessário
    get_db()
    
    logging.info("=" * 50)
    logging.info("SERVIDOR INICIADO")
    logging.info(f"Rodando em http://localhost:5000 (debug={config.DEBUG})")
    logging.info("=" * 50)
    
    app.run(host="0.0.0.0", port=5000, debug=config.DEBUG)
