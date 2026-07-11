# Playbook de Refatoração

Padrões de transformação para cada anti-pattern. Use o ID do finding do relatório para mapear a transformação correta.

---

## PT-01 — Corrigir SQL Injection (AP-01)

**Antes:**
```python
cursor.execute("SELECT * FROM usuarios WHERE email = '" + email + "' AND senha = '" + senha + "'")
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
```

**Depois:**
```python
cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
```

**Node.js — Antes:**
```javascript
db.run("INSERT INTO users (name, email) VALUES ('" + name + "', '" + email + "')")
```

**Node.js — Depois:**
```javascript
db.run("INSERT INTO users (name, email) VALUES (?, ?)", [name, email])
```

**Regra:** Todo valor externo vai como parâmetro (`?` para SQLite, `%s` para PostgreSQL). Nunca concatenado.

---

## PT-02 — Extrair Credenciais para Variáveis de Ambiente (AP-02)

**Antes:**
```python
# Em qualquer arquivo
SECRET_KEY = "minha-chave-super-secreta-123"
DB_PATH = "loja.db"
```

**Depois:**
```python
# config.py
import os

SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY não configurada")
DB_PATH = os.environ.get("DATABASE_PATH", "app.db")
```

**Node.js — Antes:**
```javascript
const config = { paymentGatewayKey: "chave-hardcoded-123" }
```

**Node.js — Depois:**
```javascript
// config.js
module.exports = {
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY
};
```

Criar arquivo `.env.example` com as variáveis necessárias (sem valores reais):
```
SECRET_KEY=
DATABASE_PATH=app.db
PAYMENT_GATEWAY_KEY=
```

---

## PT-03 — Hash de Senha (AP-03)

**Python — Antes:**
```python
cursor.execute("INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)",
               (nome, email, senha))
```

**Python — Depois:**
```python
import bcrypt

senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
cursor.execute("INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
               (nome, email, senha_hash))
```

**Verificação no login:**
```python
# Antes
cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))

# Depois
cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
usuario = cursor.fetchone()
if usuario and bcrypt.checkpw(senha.encode('utf-8'), usuario["senha_hash"].encode('utf-8')):
    return usuario
```

**Node.js — Antes:**
```javascript
const hash = badCrypto(password);
```

**Node.js — Depois:**
```javascript
const bcrypt = require('bcrypt');
const hash = await bcrypt.hash(password, 10);
// Verificação:
const match = await bcrypt.compare(password, storedHash);
```

**Remover senha das respostas:**
```python
# Nunca incluir "senha" ou "senha_hash" no dicionário retornado
def _row_to_dict(row):
    return {
        "id": row["id"],
        "nome": row["nome"],
        "email": row["email"],
        "tipo": row["tipo"]
        # sem "senha"
    }
```

> ⚠️ **PASSO OBRIGATÓRIO — Registrar nova dependência:**
> Sempre que introduzir uma biblioteca nova no código (como a de hash de senhas),
> atualize imediatamente o arquivo de dependências identificado na **Fase 1**
> (ex: `requirements.txt`, `package.json`, `Gemfile`, `go.mod`, `pom.xml`, etc.)
> usando o gerenciador de pacotes da stack detectada. Adapte o comando à linguagem do projeto.
>
> **Falhar neste passo causa erro de módulo não encontrado em qualquer instalação fresh
> do projeto — classificado como CRITICAL no catálogo de anti-patterns.**

---

## PT-04 — Decompor God Class em MVC (AP-04)

Mover cada responsabilidade para a camada correta:

| O que estava na God Class | Para onde vai |
|---|---|
| `db = sqlite3.Database(...)` | `database.py` / `database.js` |
| `CREATE TABLE ...` | `database.py` função `init_db()` |
| `SELECT/INSERT/UPDATE/DELETE` | `models/<entidade>.py` |
| Validações de negócio | `controllers/<entidade>_controller.py` |
| `app.get(...)`, `app.post(...)` | `routes/<entidade>_routes.py` |
| `app.listen()` | `app.py` / `index.js` |

**Ordem de criação dos arquivos:**
1. `database.py` (sem dependências)
2. `models/` (depende só de database)
3. `controllers/` (depende de models)
4. `routes/` (depende de controllers)
5. `app.py` (depende de routes)

---

## PT-05 — Extrair Lógica de Negócio para Controller (AP-05)

**Antes (lógica no model):**
```python
# models.py
def relatorio_vendas():
    # ... queries ...
    if faturamento > 10000:      # ← lógica de negócio no model
        desconto = faturamento * 0.1
```

**Depois (lógica no controller):**
```python
# models/pedido.py
def get_totais(db):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*), SUM(total) FROM pedidos")
    return cursor.fetchone()

# controllers/relatorio_controller.py
from config import DISCOUNT_TIER_HIGH, DISCOUNT_RATE_HIGH  # magic numbers → constantes
from models import pedido as pedido_model

def gerar_relatorio(db):
    total_pedidos, faturamento = pedido_model.get_totais(db)
    faturamento = faturamento or 0

    desconto = 0
    if faturamento > DISCOUNT_TIER_HIGH:
        desconto = faturamento * DISCOUNT_RATE_HIGH
    # ...
    return { "faturamento_bruto": faturamento, "desconto": desconto }
```

---

## PT-06 — Adicionar Transação Atômica (AP-07)

**Python — Antes:**
```python
cursor.execute("INSERT INTO pedidos ...")
pedido_id = cursor.lastrowid
cursor.execute("INSERT INTO itens_pedido ...")
cursor.execute("UPDATE produtos SET estoque = ...")
db.commit()
```

**Python — Depois:**
```python
try:
    cursor.execute("BEGIN")
    cursor.execute("INSERT INTO pedidos ...", params)
    pedido_id = cursor.lastrowid
    for item in itens:
        cursor.execute("INSERT INTO itens_pedido ...", item_params)
        cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                       (item["quantidade"], item["produto_id"]))
    db.commit()
except Exception as e:
    db.rollback()
    raise
```

**Node.js — Depois:**
```javascript
await db.run('BEGIN');
try {
    await db.run("INSERT INTO enrollments ...", params);
    await db.run("INSERT INTO payments ...", params);
    await db.run('COMMIT');
} catch (err) {
    await db.run('ROLLBACK');
    throw err;
}
```

---

## PT-07 — Resolver N+1 Queries com JOIN (AP-08)

**Antes:**
```python
cursor.execute("SELECT * FROM pedidos WHERE usuario_id = ?", (usuario_id,))
pedidos = cursor.fetchall()
for pedido in pedidos:
    cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = ?", (pedido["id"],))
    for item in cursor2.fetchall():
        cursor3.execute("SELECT nome FROM produtos WHERE id = ?", (item["produto_id"],))
```

**Depois:**
```python
cursor.execute("""
    SELECT p.id, p.status, p.total, p.criado_em,
           ip.produto_id, ip.quantidade, ip.preco_unitario,
           pr.nome as produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido ip ON ip.pedido_id = p.id
    LEFT JOIN produtos pr ON pr.id = ip.produto_id
    WHERE p.usuario_id = ?
""", (usuario_id,))
```

**Node.js — Depois:**
```javascript
db.all(`
    SELECT c.title, u.name, u.email, p.amount, p.status
    FROM courses c
    LEFT JOIN enrollments e ON e.course_id = c.id
    LEFT JOIN users u ON u.id = e.user_id
    LEFT JOIN payments p ON p.enrollment_id = e.id
`, [], callback)
```

---

## PT-08 — Centralizar Error Handling (AP-10)

**Python (Flask) — Antes:**
```python
except Exception as e:
    return jsonify({"erro": str(e)}), 500
```

**Python (Flask) — Depois:**
```python
# routes/_base.py ou app.py
@app.errorhandler(ValueError)
def handle_value_error(e):
    return jsonify({"erro": str(e)}), 400

@app.errorhandler(Exception)
def handle_generic_error(e):
    import logging
    logging.error(f"Erro inesperado: {e}", exc_info=True)
    return jsonify({"erro": "Erro interno"}), 500
```

**Node.js (Express) — Depois:**
```javascript
// middleware/errorHandler.js
module.exports = (err, req, res, next) => {
    if (err.name === 'ValidationError') {
        return res.status(400).json({ erro: err.message });
    }
    console.error(err);  // ou logger.error
    res.status(500).json({ erro: 'Erro interno' });
};

// index.js — registrar por último
app.use(require('./middleware/errorHandler'));
```

---

## PT-09 — Soft Delete (AP-11)

**Antes:**
```python
cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
```

**Depois:**
```python
# Usar o campo `ativo` já existente na tabela
cursor.execute("UPDATE produtos SET ativo = 0 WHERE id = ?", (id,))

# Filtrar inativos nas queries de listagem
cursor.execute("SELECT * FROM produtos WHERE ativo = 1")
```

Para usuários com matrículas/pedidos, verificar dependências antes:
```python
cursor.execute("SELECT COUNT(*) FROM pedidos WHERE usuario_id = ?", (usuario_id,))
count = cursor.fetchone()[0]
if count > 0:
    raise ValueError("Usuário possui pedidos e não pode ser removido")
```

---

# PT-10 — Substituir APIs Deprecated (AP-15)

**Node.js:**
```javascript
// Antes
const parsed = require('url').parse(req.url);
const buf = new Buffer(data);

// Depois
const parsed = new URL(req.url, 'http://localhost');
const buf = Buffer.from(data);
```

**Python/Flask:**
```python
# Antes
@app.before_first_request
def setup():
    init_db()

# Depois (Flask 2.3+)
with app.app_context():
    init_db()

---

## PT-11 — Remover Código Não Utilizado (AP-16)

**Estratégia:** Utilizar uma ferramenta de análise estática (linter) para identificar e, idealmente, remover automaticamente o código morto.

**Exemplo (JavaScript com ESLint):**

1. **Instalar e configurar o ESLint:**
   `npm install eslint --save-dev`
   `npx eslint --init` (e seguir as instruções para configurar o projeto)

2. **Executar a verificação:**
   `npx eslint .`

**Antes (código com variável não utilizada):**
```javascript
const express = require('express');
const { port } = require('./config'); // 'port' não é usado
const app = express();

app.listen(3000, () => console.log('Server running'));
```
**Resultado do Linter:**
```
/path/to/file.js
  2:9  error  'port' is defined but never used  no-unused-vars
```

**Depois (código corrigido):**
```javascript
const express = require('express');
// { port } removido
const app = express();

app.listen(3000, () => console.log('Server running'));
```

**Regra:** Integrar a análise de linting como um passo final da refatoração para garantir a limpeza do código. Para projetos sem linter, a inspeção manual é necessária, mas a configuração de uma ferramenta é altamente recomendada.

---

## PT-12 — Implementar Autenticação em Rotas Protegidas (AP-06)

**Python (Flask) — Decorador de Proteção de Rotas:**
```python
from functools import wraps
from flask import request, jsonify, g
from models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        
        try:
            # Em produção, usar JWT real. Para mock/fake-jwt:
            user_id = int(token.replace('Bearer fake-jwt-token-', ''))
            user = User.query.get(user_id)
            if not user or not user.active:
                return jsonify({'error': 'Acesso negado'}), 401
            g.current_user = user
        except Exception:
            return jsonify({'error': 'Token inválido'}), 401
        return f(*args, **kwargs)
    return decorated
```

**Node.js (Express) — Middleware de Proteção de Rotas:**
```javascript
const User = require('../models/user');

const tokenRequired = async (req, res, next) => {
    const authHeader = req.headers['authorization'];
    if (!authHeader) return res.status(401).json({ error: 'Token ausente' });

    try {
        const token = authHeader.replace('Bearer ', '');
        const userId = parseInt(token.replace('fake-jwt-token-', ''));
        const user = await User.getById(userId);
        if (!user || !user.active) return res.status(401).json({ error: 'Acesso negado' });
        req.user = user;
        next();
    } catch (err) {
        res.status(401).json({ error: 'Token inválido' });
    }
};
```

---

## PT-13 — Refatoração de Testes (Refactoring Tests)

**Antes (Importando a God Class monolítica e executando sem DB estruturado):**
```javascript
const AppManager = require('../src/AppManager');
const manager = new AppManager();
manager.initDb();
// ...
```

**Depois (Importando o Express App e usando Supertest com inicialização condicional e Promise-based DB):**
```javascript
const request = require('supertest');
const app = require('../app');
const database = require('../database');

beforeAll(async () => {
    await database.initDb();
});

describe('Checkout API', () => {
    it('deve cadastrar usuário com hash e salvar matrícula', async () => {
        const res = await request(app)
            .post('/api/checkout')
            .send({ usr: 'Leo', eml: 'leo@test.com', pwd: 'pwd', c_id: 1, card: '4111222233334444' });
        expect(res.status).toBe(200);
    });
});
```

**Python — Antes:**
```python
from app import app, db
# Teste que assume database global mutável
```

**Python — Depois:**
```python
import pytest
from app import app
from database import init_db

@pytest.fixture(autouse=True)
def setup_db():
    init_db()
    yield
```

---

## Ordem de Aplicação Recomendada

Sempre aplique as transformações nesta ordem para minimizar regressões:

1. **PT-02** (credenciais) — não modifica lógica, só move strings
2. **PT-01** (SQL injection) — modifica queries mas não estrutura
3. **PT-03** (hash de senha) — requer migração de dados em produção
4. **PT-04** (God Class → MVC) — reestruturação principal
5. **PT-05** (lógica → controller) — move código entre camadas
6. **PT-06** (transações) — envolve código já refatorado
7. **PT-07** (N+1 → JOIN) — otimização de queries
8. **PT-08** (error handling) — centralização transversal
9. **PT-09** (soft delete) — mudança de comportamento
10. **PT-12** (autenticação de rotas) — proteção e middlewares
11. **PT-10** (deprecated APIs) — substituições pontuais
12. **PT-11** (código não utilizado) — limpeza final com linter
13. **PT-13** (testes) — refatoração/criação de arquivos de teste para a nova arquitetura