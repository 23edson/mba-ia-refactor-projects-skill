# Análise de Projeto — Heurísticas de Detecção

## 1. Detecção de Linguagem

| Arquivo presente | Linguagem |
|---|---|
| `*.py` + `requirements.txt` | Python |
| `*.js` + `package.json` (sem `tsconfig`) | JavaScript/Node.js |
| `*.ts` + `tsconfig.json` | TypeScript/Node.js |
| `*.java` + `pom.xml` | Java/Maven |
| `*.go` + `go.mod` | Go |
| `*.rb` + `Gemfile` | Ruby |
| `*.php` + `composer.json` | PHP |

**Desempate**: se houver múltiplas linguagens, a linguagem principal é a que tem mais arquivos de lógica (excluindo configs e lock files).

---

## 2. Detecção de Framework

### Python
| Sinal | Framework |
|---|---|
| `from flask import Flask` | Flask |
| `from django.db import models` | Django |
| `from fastapi import FastAPI` | FastAPI |
| `app = Flask(__name__)` em qualquer arquivo | Flask |

### Node.js / JavaScript
| Sinal | Framework |
|---|---|
| `require('express')` ou `import express` | Express |
| `require('fastify')` | Fastify |
| `require('koa')` | Koa |
| `@nestjs/core` no `package.json` | NestJS |

### Detecção por `package.json` / `requirements.txt`
Sempre leia o arquivo de dependências — é a fonte mais confiável.
- **Node.js**: extraia os nomes das bibliotecas principais em `dependencies`.
- **Python**: liste as bibliotecas presentes no `requirements.txt`.

---

## 3. Detecção de Banco de Dados

### Heurísticas de Tabelas
Para listar as tabelas do banco:
- Busque por `CREATE TABLE` em todos os arquivos.
- Procure por strings que definam o schema (ex: `cursor.execute("CREATE TABLE IF NOT EXISTS ...")`).
- Em projetos com ORM, liste as classes que herdam de `db.Model` ou similar.
- Se houver um arquivo `.sql` de setup, ele é a melhor fonte.

### Heurísticas de Driver
| Sinal no código | Banco |
|---|---|
| `sqlite3`, `':memory:'`, `loja.db` | SQLite |
| `psycopg2`, `pg`, `postgresql://` | PostgreSQL |
| `mysql`, `mysql2`, `pymysql` | MySQL |
| `mongoose`, `mongodb` | MongoDB |
| `sequelize`, `typeorm`, `sqlalchemy` | ORM (detectar banco pelo config) |

---

## 4. Mapeamento de Arquitetura

### Sinais de arquivo por responsabilidade

**Acesso a dados (candidatos a Model):**
- Contém `SELECT`, `INSERT`, `UPDATE`, `DELETE`
- Importa driver de banco (`sqlite3`, `psycopg2`, `mysql2`)
- Funções com nomes como `get_*`, `create_*`, `update_*`, `delete_*`
- Contém `cursor.execute()` ou `.query()`
- Contém definições de tabelas ou esquemas de dados.

**Rotas (candidatos a View/Routes):**
- Contém `@app.route`, `app.get(`, `app.post(`
- Importa `request`, `response`, `req`, `res`
- Retorna `jsonify()`, `res.json()`, `res.send()`
- Registra endpoints HTTP

**Lógica de negócio (candidatos a Controller):**
- Contém validações de negócio (ex: verificar estoque, calcular desconto)
- Orquestra múltiplas chamadas a dados
- Contém regras condicionais complexas baseadas em estado de negócio

**Entry point:**
- Contém `app.run()`, `app.listen()`, `server.listen()`
- Geralmente `app.py`, `main.py`, `index.js`, `server.js`

---

## 5. Classificação de Arquitetura Atual

| Classificação | Sinais |
|---|---|
| **Monolítica** | 1-2 arquivos com tudo misturado (rotas + SQL + lógica) |
| **Parcialmente separada** | Existe alguma separação, mas camadas ainda misturadas |
| **MVC incompleto** | Estrutura de pastas existe mas responsabilidades vazam entre camadas |
| **MVC** | Models, Controllers e Routes claramente separados e com responsabilidades corretas |

---

## 6. Checklist de Análise Completa

Antes de passar para a Fase 2, confirme que você identificou:

- [ ] Linguagem e versão (se disponível no config)
- [ ] Framework principal
- [ ] Banco de dados e forma de acesso (raw SQL vs ORM)
- [ ] Principais tabelas identificadas
- [ ] Principais dependências identificadas
- [ ] Entry point da aplicação
- [ ] Todos os arquivos com sua responsabilidade atual
- [ ] Número total de arquivos analisados
- [ ] Domínio da aplicação (e-commerce, LMS, task manager, etc.)