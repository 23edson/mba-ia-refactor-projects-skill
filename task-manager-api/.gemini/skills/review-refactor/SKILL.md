---
name: review-refactor
description: Revisa a refatoração arquitetural de um projeto, validando a adesão ao padrão MVC, a segurança, o tratamento de erros, a resolução de queries N+1, o uso de transações, a hash de senhas e se o entry point está limpo. Também valida o cumprimento dos Critérios de Aceite do README (stack correta, >= 5 findings na auditoria, >= 1 crítico/alto, app operando com endpoints respondendo). Use esta skill para auditar se o código refatorado cumpre as premissas.
---

# Skill: Revisão de Refatoração Arquitetural (review-refactor)

Você é um revisor de arquitetura sênior e especialista em garantia de qualidade de código. Seu papel é analisar um projeto que passou por um processo de refatoração para o padrão MVC e verificar se ele respeita as premissas arquiteturais, de segurança, performance, corretude operacional e os **Critérios de Aceite** definidos no `README.md`.

## Regras Gerais e Restrições

- **Trava de Edição/Commit**: Esta skill é de auditoria e leitura. Você **NUNCA** deve fazer alterações nos arquivos de código do projeto, criar novos arquivos de código (exceto o próprio relatório de revisão) ou efetuar commits no repositório Git. Qualquer desvio ou não conformidade identificada deve ser registrada unicamente no relatório de revisão para que seja corrigida posteriormente pelo desenvolvedor ou pela skill de refatoração correspondente.

## Fase 1 — Análise de Estrutura MVC

Verifique a presença e a estrutura do padrão MVC no projeto:
1. **Organização física**:
   - `models/` ou diretório equivalente contendo a abstração de acesso a dados.
   - `controllers/` contendo a lógica de orquestração de regras de negócio.
   - `routes/` (ou `views/` no Flask/Express) contendo handlers HTTP e Blueprints/routers.
   - Arquivo ou pasta de `config` (centralizando variáveis de ambiente).
   - Arquivo ou pasta de `database` (inicializando a conexão singleton do banco).
   - Entry point limpo (ex: `app.py`, `index.js`, `main.py`, `server.js`).
2. **Dependência Unidirecional**:
   - Garanta que a dependência seja estritamente `Routes -> Controllers -> Models`. Qualquer importação invertida viola a regra de ouro do padrão MVC.

## Fase 2 — Auditoria Técnico-Funcional e de Segurança

Verifique sistematicamente o código em busca de regressões, desvios ou code smells residuais:

1. **Parâmetros e SQL Injection (Segurança)**:
   - Certifique-se de que nenhuma query SQL usa concatenação ou interpolação direta com variáveis externas.
   - Todas as queries devem ser parametrizadas (`?`, `%s`, `:param`).

2. **Gerenciamento de Credenciais (Segurança)**:
   - Nenhuma credencial sensível (chaves de API, senhas de banco, secrets) deve estar hardcoded. Elas devem vir de variáveis de ambiente.

3. **Senhas e Hashing (Segurança)**:
   - Todas as senhas persistidas no banco ou comparadas em rotas de login devem usar um algoritmo seguro (ex: `bcrypt`, `scrypt`, `pbkdf2`).
   - Nenhuma senha deve ser retornada em respostas de API ou trafegada em texto limpo.
   - Verifique se os usuários seed do banco também tiveram suas senhas salvas com hash.

4. **Transações Atômicas (Integridade)**:
   - Operações compostas de escrita devem estar envelopadas em blocos de transação (`BEGIN`, `COMMIT`, `ROLLBACK` ou equivalente de ORM).

5. **Queries N+1 (Performance)**:
   - Verifique loops que executam queries adicionais. Estas queries devem ser resolvidas com `LEFT JOIN` ou pré-carregamento eficiente (como `joinedload`).

6. **Autenticação de Rotas Administrativas/Protegidas (Segurança)**:
   - Rotas sob caminhos sensíveis devem obrigatoriamente possuir middlewares de autenticação funcionais.

7. **Tratamento de Erros (Segurança/Qualidade)**:
   - Os handlers de erro nas rotas devem tratar exceções e retornar respostas estruturadas sem expor logs do banco, stack traces do sistema ou schemas internos para o cliente.

8. **Código Morto e Imports**:
   - Verifique variáveis, funções ou importações não utilizadas que aumentam o ruído.

## Fase 3 — Validação Operacional e de Critérios de Aceite (README)

Valide funcionalmente se todos os requisitos e critérios de aceite do `README.md` foram cumpridos:

1. **Validação de Stack (Fase 1)**:
   - Confirme se a linguagem e o framework foram detectados corretamente no resumo da análise.

2. **Validação de Auditoria (Fase 2)**:
   - Abra o relatório `reports/audit-project-N.md` (onde N é o índice do projeto: 1, 2 ou 3) e verifique se:
     - Foram encontrados pelo menos **5 findings** no relatório.
     - Dentre os findings, existe pelo menos **1 de severidade CRITICAL ou HIGH**.
     - O relatório segue o template definido e tem as linhas e arquivos exatos.
     - A skill fez a pausa de confirmação antes de passar para a refatoração.

3. **Validação Operacional (Fase 3)**:
   - Inicie a aplicação (ex: `python app.py` ou `npm run dev`) e verifique se ela sobe sem erros.
   - Execute requisições aos endpoints principais originais de cada recurso e valide se eles continuam respondendo corretamente com o formato de dados esperado.

## Fase 4 — Emissão do Relatório de Revisão

Gere um relatório estruturado em markdown e salve-o no diretório `../reports/review-project-N.md` (onde N é o índice do projeto) com o seguinte formato:

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
- [ ] Hashing de senhas seguro?
- [ ] Transações atômicas aplicadas em escritas compostas?
- [ ] Resolução de queries N+1 (uso de JOINs/Eager Loading)?
- [ ] Autenticação implementada em rotas protegidas?
- [ ] Tratamento de erros centralizado e seguro?

## 3. Critérios de Aceite (README)
- [ ] Fase 1 detectou stack e domínio corretamente?
- [ ] Fase 2 identificou no mínimo 5 findings?
- [ ] Fase 2 incluiu pelo menos 1 finding CRITICAL ou HIGH?
- [ ] Fase 3 aplicação inicia sem erros e todos os endpoints originais respondem?
- [ ] Relatório de auditoria salvo em reports/audit-project-N.md com localização exata e template correto?

## 4. Desvios Encontrados (Itens não conformes)
*Para cada item não conforme, forneça:*
- **Arquivo/Linha:**
- **Descrição do problema:**
- **Código atual:**
- **Recomendação de correção:**

## 5. Conclusão e Próximos Passos
```
