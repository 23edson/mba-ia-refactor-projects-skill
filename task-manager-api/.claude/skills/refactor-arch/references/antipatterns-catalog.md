# Catálogo de Anti-Patterns

Cada anti-pattern tem: descrição, severidade, sinais de detecção (o que buscar no código), e impacto.

---

## CRITICAL

### AP-01 — SQL Injection
**Severidade:** CRITICAL  
**Descrição:** Queries SQL construídas por concatenação de strings com entrada do usuário.

**Sinais de detecção:**
- `"SELECT ... WHERE id = " + str(id)`
- `"WHERE email = '" + email + "'"`
- `cursor.execute("..." + variavel + "...")`
- Qualquer f-string ou `.format()` dentro de `cursor.execute()`
- `db.run("... " + req.body.algo + " ...")`

**Impacto:** Permite acesso, modificação ou destruição total do banco de dados.

**Não confundir com:** Queries parametrizadas com `?` ou `%s` são seguras.

---

### AP-02 — Credenciais Hardcoded
**Severidade:** CRITICAL  
**Descrição:** Senhas, chaves de API, secrets ou tokens escritos diretamente no código-fonte.

**Sinais de detecção:**
- `secret_key = "valor-literal"`
- `password = "123"` ou `pass = "abc"`
- `API_KEY = "sk-..."` ou `paymentGatewayKey = "..."`
- Qualquer string que pareça uma chave/token em atribuição de variável
- Credenciais expostas em respostas de API (ex: endpoint `/health` retornando `secret_key`)

**Impacto:** Exposição de infraestrutura, contas financeiras e dados de usuários.

---

### AP-03 — Senhas em Texto Puro
**Severidade:** CRITICAL  
**Descrição:** Senhas armazenadas ou comparadas sem hash criptográfico.

**Sinais de detecção:**
- `INSERT INTO users (..., senha) VALUES (..., senha_do_usuario)`
- `WHERE senha = '" + senha + "'`
- Coluna `pass`, `password`, `senha` sem nenhum hash antes do INSERT
- Login comparando campo de senha diretamente: `AND senha = ?`
- Função com nome `badCrypto`, `simpleHash` ou similar
- Senha retornada em respostas da API (`"senha": row["senha"]`)

**Impacto:** Exposição de todas as senhas em caso de vazamento do banco.

---

### AP-04 — God Class / Monolito
**Severidade:** CRITICAL  
**Descrição:** Uma única classe ou arquivo concentra responsabilidades de banco de dados, rotas, lógica de negócio e configuração.

**Sinais de detecção:**
- Arquivo único com mais de 200 linhas contendo `SELECT`, `app.get(`, e regras de negócio
- Classe que inicializa banco E define rotas E processa pagamentos
- `setupRoutes()` dentro da mesma classe que faz `db.run()`
- Controllers que importam diretamente o driver do banco (`import sqlite3`, `require('sqlite3')`)

**Impacto:** Impossível testar unitariamente, alterar sem risco de regressão, ou reutilizar lógica.

---

## HIGH

### AP-05 — Lógica de Negócio em Controller/Route
**Severidade:** HIGH  
**Descrição:** Regras de negócio complexas (cálculos, validações de domínio, orquestração) implementadas diretamente no handler de rota.

**Sinais de detecção:**
- Cálculos financeiros (`desconto = faturamento * 0.1`) dentro de funções que retornam `jsonify()` ou `res.json()`
- Validação de estoque, cálculo de total de pedido dentro do controller
- Lógica condicional complexa de negócio antes do `return res.status(200)`
- `print("ENVIANDO EMAIL/SMS/PUSH...")` dentro de route handlers

**Impacto:** Lógica não reutilizável, impossível de testar sem HTTP, viola SRP.

---

### AP-06 — Sem Autenticação em Rotas Protegidas
**Severidade:** HIGH  
**Descrição:** Endpoints administrativos ou que expõem dados sensíveis sem verificação de identidade.

**Sinais de detecção:**
- Rotas com `/admin`, `/report`, `/financeiro` sem middleware de auth
- `listar_todos_usuarios()`, `relatorio_vendas()` sem verificação de token/sessão
- Nenhum `req.headers.authorization` ou verificação de sessão em nenhuma rota
- Ausência total de qualquer middleware de autenticação no projeto

**Impacto:** Qualquer pessoa pode acessar dados sensíveis ou executar ações privilegiadas.

---

### AP-07 — Sem Transação em Operações Compostas
**Severidade:** HIGH  
**Descrição:** Operações que envolvem múltiplas escritas no banco executadas sem transação atômica.

**Sinais de detecção:**
- Múltiplos `cursor.execute()` ou `db.run()` em sequência sem `BEGIN`/`COMMIT`/`ROLLBACK`
- Ausência de `try/except` com `db.rollback()` em operações de criação de pedido, pagamento, matrícula
- `db.commit()` chamado múltiplas vezes dentro da mesma operação lógica
- Sem tratamento de falha entre INSERT de pedido e INSERT de itens

**Impacto:** Dados inconsistentes em caso de falha parcial (pedido criado sem itens, estoque decrementado sem pedido).

---

## MEDIUM

### AP-08 — N+1 Queries
**Severidade:** MEDIUM  
**Descrição:** Uma query inicial retorna N registros, e para cada registro é feita uma query adicional dentro de um loop.

**Sinais de detecção:**
- `cursor.execute(...)` ou `db.get(...)` dentro de `for row in rows:` ou `.forEach()`
- Múltiplos cursors abertos dentro de loop (`cursor2`, `cursor3`)
- Buscar nome/detalhes de entidade relacionada um por um dentro de iteração
- Padrão: query de lista → loop → query de detalhe por ID

**Impacto:** Performance degrada linearmente (ou pior) com volume de dados.

---

### AP-09 — Validação Duplicada entre Camadas
**Severidade:** MEDIUM  
**Descrição:** As mesmas regras de validação implementadas em múltiplos lugares (controller e model, por exemplo), ou validação presente em uma camada mas ausente em outra.

**Sinais de detecção:**
- `if preco < 0` no controller E sem validação equivalente no model
- Validação de campos obrigatórios repetida em `criar_produto` e `atualizar_produto`
- Enum de status válidos definido no controller mas não no model
- Ausência de validação de formato (email, CPF, etc.) em qualquer camada

**Impacto:** Inconsistência quando model é chamado diretamente; manutenção dobrada.

---

### AP-10 — Erro Interno Exposto ao Cliente
**Severidade:** MEDIUM  
**Descrição:** Mensagens de exceção do sistema retornadas diretamente na resposta HTTP.

**Sinais de detecção:**
- `return jsonify({"erro": str(e)}), 500`
- `res.status(500).send(err.message)`
- Stack trace ou mensagem de exception do banco exposta na resposta
- `except Exception as e: return {"erro": str(e)}`

**Impacto:** Vaza detalhes de schema do banco, paths do sistema, versões de bibliotecas.

---

### AP-11 — Hard Delete sem Verificação de Integridade
**Severidade:** MEDIUM  
**Descrição:** Deleção permanente de registros que possuem dependências em outras tabelas, sem verificar ou tratar referências.

**Sinais de detecção:**
- `DELETE FROM users WHERE id = ?` sem verificar `enrollments`, `pedidos`, `pagamentos`
- `deletar_produto` sem checar `itens_pedido`
- Ausência de `ON DELETE CASCADE` ou soft delete para entidades com relacionamentos

**Impacto:** Dados órfãos corrompem relatórios e podem causar erros em queries futuras.

---

## LOW

### AP-12 — Magic Numbers
**Severidade:** LOW  
**Descrição:** Valores numéricos literais sem nome que representam regras de negócio ou limiares.

**Sinais de detecção:**
- `if faturamento > 10000:`, `if faturamento > 5000:`
- `desconto = faturamento * 0.1` sem constante nomeada
- Qualquer número que não seja 0 ou 1 em condicionais de negócio

**Impacto:** Dificulta alteração e entendimento da regra de negócio.

---

### AP-13 — Console/Print como Logging
**Severidade:** LOW  
**Descrição:** Uso de `print()` ou `console.log()` como único mecanismo de registro de eventos e erros.

**Sinais de detecção:**
- `print("ERRO: " + str(e))` como único tratamento de exceção
- `console.log(...)` para registrar operações críticas
- Ausência de `import logging` (Python) ou biblioteca de log estruturado (Node.js)
- `print("ENVIANDO EMAIL...")` simulando operações reais

**Impacto:** Sem nível, sem timestamp, sem persistência. Dificulta diagnóstico em produção.

---

### AP-14 — Shadowing de Built-ins / Nomenclatura Problemática
**Severidade:** LOW  
**Descrição:** Uso de nomes de variáveis que conflitam com built-ins da linguagem ou são excessivamente abreviados.

**Sinais de detecção (Python):**
- `id = models.criar_produto(...)` — `id` é built-in do Python
- `list = [...]`, `type = "..."`, `input = dados.get(...)`

**Sinais de detecção (JavaScript/Node.js):**
- `let u, e, p, cid, cc` — abreviações sem contexto
- Variáveis de uma letra fora de loops simples

**Impacto:** Comportamento inesperado (Python: `id()` built-in sobrescrito); dificuldade de leitura.

---

### AP-15 — API Deprecated / Obsoleta
**Severidade:** LOW  
**Descrição:** Uso de APIs, métodos ou padrões que foram descontinuados na versão atual da linguagem ou framework.

**Sinais de detecção (Python/Flask):**
- `@app.before_first_request` → removido no Flask 2.3+, usar `with app.app_context()`
- `flask.ext.*` → removido no Flask 1.0+
- `db.session.query(Model)` (estilo legado SQLAlchemy) → preferir `select(Model)`

**Sinais de detecção (Node.js):**
- `require('url').parse()` → deprecado, usar `new URL()`
- `new Buffer()` → deprecado, usar `Buffer.from()` / `Buffer.alloc()`
- `domain` module → deprecado
- Callbacks em vez de Promises/async-await em APIs modernas do Node

**Impacto:** Pode quebrar em atualizações futuras; warnings em runtime; segurança em alguns casos.

---

### AP-16 — Código Não Utilizado (Unused Code)
**Severidade:** LOW  
**Descrição:** Variáveis, funções ou imports declarados mas nunca utilizados no escopo do arquivo.

**Sinais de detecção:**
- `import { algo } from 'lib'` onde `algo` não é usado.
- `const variavel = "valor"` onde `variavel` nunca é lida.
- `function util(a, b)` que nunca é chamada.
- Detecção automatizada por ferramentas de linting (ESLint, Pyflakes, etc.).

**Impacto:** Aumenta o "ruído" no código, tornando-o mais difícil de entender e manter. Pode levar a um aumento no tamanho do bundle em aplicações front-end.

---

### AP-17 — Desvio de Camada em Middlewares / Guards (Bypass de Controller)
**Severidade:** MEDIUM  
**Descrição:** Middlewares, decorators ou interceptores de rota que realizam operações de banco de dados diretamente acessando Models ou Driver SQL, contornando a camada de Controller.

**Sinais de detecção:**
- Importar `database.get_db` ou models diretamente em decoradores de rota (ex: `from models import usuario as usuario_model`).
- Fazer chamadas diretas como `usuario_model.get_usuario_por_id(...)` dentro de middlewares (`token_required`, `admin_required`, `auth_helper`).
- Executar `cursor.execute(...)` ou consultas SQL diretamente em middlewares de rotas.

**Impacto:** Quebra o princípio da separação de responsabilidades (MVC) e acopla a camada de entrega (HTTP/Rotas) diretamente aos detalhes de banco de dados, duplicando lógica de validação ou de negócio que deveria estar centralizada no Controller.
