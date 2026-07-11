import logging
import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from database import db
from config import Config
from routes.task_routes import task_bp
from routes.user_routes import user_bp
from routes.report_routes import report_bp
from routes.category_routes import category_bp

# Configura o sistema de logging padrão (Finding L-1 / AP-13)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)

# Registro de rotas
app.register_blueprint(task_bp)
app.register_blueprint(user_bp)
app.register_blueprint(report_bp)
app.register_blueprint(category_bp)

@app.route('/health')
def health():
    return {'status': 'ok', 'timestamp': str(datetime.datetime.now())}

@app.route('/')
def index():
    return {'message': 'Task Manager API', 'version': '1.0'}

# Centralizador de exceções genéricas para evitar vazamento de dados internos (Finding M-3 / AP-10)
@app.errorhandler(Exception)
def handle_unexpected_error(e):
    logger.error(f"Erro não tratado na aplicação: {e}", exc_info=True)
    return jsonify({'error': 'Erro interno do servidor'}), 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
