# Guidelines de Arquitetura MVC

> **⚠️ Escopo desta Skill — MVC Clássico (3 Camadas)**
>
> Esta skill adota intencionalmente o **MVC clássico de 3 camadas** (Routes → Controllers → Models) como padrão-alvo.
> Neste modelo, os **Controllers concentram tanto a orquestração quanto as regras de negócio**, o que é adequado para APIs simples e para fins educacionais.
>
> Em projetos de médio/grande porte, recomenda-se evoluir para uma arquitetura de 4 camadas introduzindo uma camada de **Services**
> (Routes → Controllers → Services → Models), onde:
> - **Controller** apenas valida o payload HTTP e mapeia o retorno para status codes.
> - **Service** contém exclusivamente a lógica de negócio, agnóstica de protocolo (não conhece `request`, `response` ou `jsonify`).
>
> Esta separação adicional está **fora do escopo deste desafio** e não deve ser implementada durante a refatoração.

## O Padrão Alvo

```
projeto/
├── app.py / index.js          ← Entry point: inicializa app e registra rotas
├── config.py / config.js      ← Configurações centralizadas
├── database.py / database.js  ← Conexão com banco (singleton)
├── models/                    ← Camada de dados
│   ├── __init__.py (Python)
│   ├── produto.py / produto.js
│   └── usuario.py / usuario.js
├── controllers/               ← Camada de lógica de negócio
│   ├── __init__.py (Python)
│   ├── produto_controller.py
│   └── usuario_controller.py
├── routes/                    ← Camada de roteamento HTTP
│   ├── __init__.py (Python)
│   ├── produto_routes.py
│   └── usuario_routes.py
└── requirements.txt / package.json
```

---

## Responsabilidades de Cada Camada

### Model (`models/`)
**Responsabilidade única:** Abstração do acesso a dados.

✅ **DEVE:**
- Executar queries SQL parametrizadas
- Mapear rows do banco para dicionários/objetos
- Funções CRUD básicas por entidade
- Tratar erros de banco e relançar como exceções de domínio

❌ **NÃO DEVE:**
- Conter regras de negócio (cálculo de desconto, validação de estoque)
- Conhecer HTTP (request, response, status codes)
- Fazer validação de input do usuário
- Chamar outros models diretamente (isso é responsabilidade do Controller)

**Exemplo Python:**
```python
# models/produto.py
def get_por_id(db, produto_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    return cursor.fetchone()

def criar(db, nome, descricao, preco, estoque, categoria):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
        (nome, descricao, preco, estoque, categoria)
    )
    db.commit()
    return cursor.lastrowid
```

---

### Controller (`controllers/`)
**Responsabilidade única:** Orquestração da lógica de negócio.

✅ **DEVE:**
- Receber dados já extraídos da request (não o objeto `request` inteiro)
- Validar regras de negócio (estoque suficiente, preço válido, etc.)
- Coordenar múltiplos models para operações complexas
- Gerenciar transações quando necessário
- Retornar dados de domínio (dicionários, objetos), nunca respostas HTTP

❌ **NÃO DEVE:**
- Conhecer HTTP (`request`, `response`, `jsonify`, `res.json()`)
- Executar queries SQL diretamente
- Fazer logging de infraestrutura (use o módulo de logging)
- Enviar emails, SMS, push notifications (delegue para serviços)

**Exemplo Python:**
```python
# controllers/pedido_controller.py
from models import produto as produto_model
from models import pedido as pedido_model

def criar_pedido(db, usuario_id, itens):
    total = 0
    for item in itens:
        produto = produto_model.get_por_id(db, item["produto_id"])
        if produto is None:
            raise ValueError(f"Produto {item['produto_id']} não encontrado")
        if produto["estoque"] < item["quantidade"]:
            raise ValueError(f"Estoque insuficiente para {produto['nome']}")
        total += produto["preco"] * item["quantidade"]

    return pedido_model.criar(db, usuario_id, itens, total)
```

---

### Routes (`routes/`)
**Responsabilidade única:** Definição de endpoints HTTP e delegação ao Controller.

✅ **DEVE:**
- Extrair dados da `request` (body, params, query string)
- Chamar o Controller correspondente
- Converter resultado do Controller em resposta HTTP
- Tratar exceções do Controller e mapear para status codes HTTP
- Validar presença de campos obrigatórios no payload HTTP

❌ **NÃO DEVE:**
- Conter lógica de negócio
- Acessar banco de dados diretamente
- Conhecer detalhes de implementação do Model

**Exemplo Python (Flask):**
```python
# routes/produto_routes.py
from flask import Blueprint, request, jsonify
from controllers import produto_controller

produto_bp = Blueprint("produtos", __name__)

@produto_bp.route("/produtos/<int:id>", methods=["GET"])
def buscar_produto(id):
    try:
        produto = produto_controller.get_por_id(id)
        if not produto:
            return jsonify({"erro": "Produto não encontrado"}), 404
        return jsonify({"dados": produto}), 200
    except Exception:
        return jsonify({"erro": "Erro interno"}), 500
```

**Exemplo Node.js (Express):**
```javascript
// routes/produto_routes.js
const express = require('express');
const router = express.Router();
const produtoController = require('../controllers/produto_controller');

router.get('/:id', async (req, res) => {
    try {
        const produto = await produtoController.getById(req.params.id);
        if (!produto) return res.status(404).json({ erro: 'Produto não encontrado' });
        res.json({ dados: produto });
    } catch (err) {
        res.status(500).json({ erro: 'Erro interno' });
    }
});

module.exports = router;
```

---

### Config (`config.py` / `config.js`)
**Responsabilidade:** Centralizar toda configuração da aplicação.

```python
# config.py
import os

DATABASE_PATH = os.environ.get("DATABASE_PATH", "app.db")
SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"

# Tiers de desconto
DISCOUNT_TIER_HIGH = 10000
DISCOUNT_TIER_MID = 5000
DISCOUNT_TIER_LOW = 1000
DISCOUNT_RATE_HIGH = 0.10
DISCOUNT_RATE_MID = 0.05
DISCOUNT_RATE_LOW = 0.02
```

```javascript
// config.js
module.exports = {
    dbPath: process.env.DATABASE_PATH || 'app.db',
    secretKey: process.env.SECRET_KEY,
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY,
    debug: process.env.DEBUG === 'true'
};
```

---

### Entry Point (`app.py` / `index.js`)
**Responsabilidade:** Inicializar a aplicação e registrar rotas. Deve ser o arquivo mais simples do projeto.

```python
# app.py
from flask import Flask
from database import init_db
from routes.produto_routes import produto_bp
from routes.usuario_routes import usuario_bp

app = Flask(__name__)
app.register_blueprint(produto_bp, url_prefix="/api/produtos")
app.register_blueprint(usuario_bp, url_prefix="/api/usuarios")

if __name__ == "__main__":
    init_db()
    app.run(debug=False)
```

---

## Regras de Ouro

1. **Dependência unidirecional**: Routes → Controllers → Models. Nunca ao contrário.
2. **Controllers não conhecem HTTP**: se um controller recebe `request` ou retorna `jsonify()`, está errado.
3. **Models não conhecem negócio**: se um model calcula desconto ou valida estoque, está errado.
4. **Configuração nunca no código**: toda string mágica vai para `config.py` ou variável de ambiente.
5. **Erros de domínio vs HTTP**: Controllers lançam exceções de domínio (`ValueError`, `NotFoundError`); Routes convertem para status HTTP.