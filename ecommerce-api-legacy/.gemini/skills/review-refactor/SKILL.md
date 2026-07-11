---
name: review-refactor
description: Revisa a refatoração arquitetural de um projeto, validando a adesão ao padrão MVC, a segurança, o tratamento de erros, a resolução de queries N+1, o uso de transações, a hash de senhas e se o entry point está limpo. Use esta skill para auditar se o código refatorado cumpre as premissas arquiteturais e de qualidade de código sem quebrar a aplicação.
---

# Skill: Revisão de Refatoração Arquitetural (review-refactor)

Você é um revisor de arquitetura sênior e especialista em garantia de qualidade de código. Seu papel é analisar um projeto que passou por um processo de refatoração para o padrão MVC e verificar se ele respeita as premissas arquiteturais, de segurança, performance e corretude operacional definidas.

## Fase 1 — Análise de Estrutura MVC

Verifique a presença e a estrutura do padrão MVC no projeto:
1. **Organização física**:
   - `models/` ou diretório equivalente contendo a prisão de acesso a dados.
   - `controllers/` contendo a lógica de orquestração de regras de negócio.
   - `routes/` (ou `views/` no Flask/Express) contendo handlers HTTP e Blueprints/routers.
   - Arquivo ou pasta de `config` (centralizando variáveis de ambiente).
   - Arquivo ou pasta de `database` (inicializando a conexão singleton do banco).
   - Entry point limpo (ex: `app.py`, `index.js`, `main.py`, `server.js`).
2. **Dependência Unidirecional**:
   - Garanta que a dependência seja estritamente `Routes -> Controllers -> Models`. Qualquer importação invertida (ex: Models importando Controllers ou Controllers importando Routes) viola a regra de ouro do padrão MVC.

## Fase 2 — Auditoria Técnico-Funcional e de Segurança

Verifique sistematicamente o código em busca de regressões, desvios ou code smells residuais:

1. **Parâmetros e SQL Injection (Segurança)**:
   - Certifique-se de que nenhuma query SQL usa concatenação ou interpolação direta com variáveis externas (ex: f-strings com input do usuário ou concatenação com `+`).
   - Todas as queries devem ser parametrizadas (`?`, `%s`, `:param` dependendo do banco/driver).

2. **Gerenciamento de Credenciais (Segurança)**:
   - Nenhuma credencial sensível (chaves de API, senhas de banco, secrets) deve estar hardcoded. Elas devem vir de variáveis de ambiente.
   - Verifique também se as chaves em seeds de banco ou fallbacks de arquivo de config não contêm segredos reais ou senhas expostas.

3. **Senhas e Hashing (Segurança)**:
   - Todas as senhas persistidas no banco ou comparadas em rotas de login devem usar um algoritmo seguro (ex: `bcrypt`).
   - Nenhuma senha deve ser retornada em respostas de API ou trafegada em texto limpo.
   - Verifique se os usuários seed do banco também tiveram suas senhas salvas com hash.

4. **Transações Atômicas (Integridade)**:
   - Operações compostas de escrita (ex: criação de pedido com inserção de itens de pedido e decremento de estoque, ou checkout que insere matrícula e pagamento) devem estar envelopadas em blocos de transação (`BEGIN`, `COMMIT`, `ROLLBACK` ou equivalente de ORM).

5. **Queries N+1 (Performance)**:
   - Verifique loops que executam queries adicionais (ex: `.forEach()` ou `for` que consulta dados relacionados por ID).
   - Essas queries devem ser resolvidas com `LEFT JOIN` ou pré-carregamento eficiente.

6. **Autenticação de Rotas Administrativas/Protegidas (Segurança)**:
   - Rotas sob caminhos sensíveis (ex: `/admin`, `/reports`, deleção de usuários) devem obrigatoriamente possuir middlewares de autenticação funcionais.
   - Placeholders ou mocks de autenticação que apenas liberam o tráfego com logs não são válidos.

7. **Tratamento de Erros (Segurança/Qualidade)**:
   - Os handlers de erro nas rotas devem tratar exceções e retornar respostas estruturadas sem expor logs do banco, stack traces do sistema ou schemas internos para o cliente final.

8. **Código Morto e Imports**:
   - Verifique variáveis, funções ou importações não utilizadas que aumentam o ruído.

## Fase 3 — Validação Operacional

Execute a verificação prática de boot e conformidade:
1. Tente iniciar a aplicação.
2. Certifique-se de que a aplicação sobe sem erros de importação ou execução.
3. Teste o funcionamento básico dos endpoints principais de cada recurso.

## Fase 4 — Emissão do Relatório de Revisão

Gere um relatório estruturado em markdown e salve-o no diretório `../reports/review-project-N.md` (onde N é o índice do projeto: 1, 2 ou 3) com o seguinte formato:

```markdown
# Relatório de Revisão de Refatoração MVC

**Projeto:** <nome-do-projeto>
**Status Geral:** [CONFORME | PARCIALMENTE CONFORME | NÃO CONFORME]

## 1. Avaliação Estrutural
- [ ] Estrutura MVC implementada de forma coerente?
- [ ] Entry point limpo?
- [ ] Configurações extraídas?

## 2. Checklist Técnico e de Segurança
- [ ] Queries parametrizadas (Sem SQL Injection)?
- [ ] Credenciais e variáveis de ambiente isoladas?
- [ ] Hashing de senhas seguro (Bcrypt)?
- [ ] Transações atômicas aplicadas em escritas compostas?
- [ ] Resolução de queries N+1 (uso de JOINs)?
- [ ] Autenticação implementada em rotas protegidas?
- [ ] Tratamento de erros centralizado e seguro?

## 3. Desvios Encontrados (Itens não conformes)
*Para cada item não conforme, forneça:*
- **Arquivo/Linha:**
- **Descrição do problema:**
- **Código atual:**
- **Recomendação de correção:**

## 4. Conclusão e Próximos Passos
```
