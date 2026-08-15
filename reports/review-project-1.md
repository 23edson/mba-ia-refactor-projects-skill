# Relatório de Revisão de Refatoração MVC

**Projeto:** code-smells-project
**Status Geral:** CONFORME

## 1. Avaliação Estrutural
- [x] Estrutura MVC implementada de forma coerente?  
  *Sim, o projeto está estruturado nos diretórios `models/`, `controllers/` e `routes/`. O entrypoint, a base de dados e a configuração foram centralizados e limpos.*
- [x] Entry point limpo?  
  *Sim, `app.py` agora serve apenas para inicializar o Flask, registrar os blueprints de rotas e definir o tratamento global de exceções.*
- [x] Configurações extraídas?  
  *Sim, `config.py` utiliza `python-dotenv` para carregar as variáveis de ambiente e gerenciar configurações com segurança.*

## 2. Checklist Técnico e de Segurança
- [x] Queries parametrizadas (Sem SQL Injection)?  
  *Sim, todas as queries no banco de dados SQLite utilizam parametrização com placeholders (`?`), prevenindo ataques de SQL Injection.*
- [x] Credenciais e variáveis de ambiente isoladas?  
  *Sim, segredos como `SECRET_KEY` são carregados do arquivo `.env` via variáveis de ambiente, sem fallbacks vulneráveis no código.*
- [x] Hashing de senhas seguro (Bcrypt)?  
  *Sim, as senhas de usuários novos e as senhas do seed do banco de dados são salvas no formato hash via `bcrypt`.*
- [x] Transações atômicas aplicadas em escritas compostas?  
  *Sim, o modelo `models/pedido.py` envelopa a criação do pedido, inserção dos itens e dedução do estoque em um bloco de transação segura com `BEGIN TRANSACTION`, `commit()` e `rollback()` em caso de falha.*
- [x] Resolução de queries N+1 (uso de JOINs)?  
  *Sim, a listagem de pedidos utiliza `LEFT JOIN` nas tabelas `itens_pedido` e `produtos` para buscar todos os dados relacionados em uma única consulta ao banco.*
- [x] Autenticação implementada em rotas protegidas?  
  *Sim, todas as rotas de usuários, pedidos, relatórios e administrativas utilizam decoradores (`@token_required` e `@admin_required`) com assinatura criptográfica de tokens JWT reais.*
- [x] Tratamento de erros centralizado e seguro?  
  *Sim, os tratamentos globais de exceção no Flask evitam o vazamento de stack traces e schemas do banco de dados para os clientes.*

## 3. Comparação com o Relatório de Auditoria (audit-project-1.md)
- [x] Todos os pontos CRITICAL do relatório de auditoria foram resolvidos?
- [x] Todos os pontos HIGH do relatório de auditoria foram resolvidos?
- [x] Todos os pontos MEDIUM do relatório de auditoria foram resolvidos?
- [x] Todos os pontos LOW do relatório de auditoria foram resolvidos?

### Detalhes das Correções:
* **[C-1] Credenciais Hardcoded / Fallback Inseguro:** Resolvido no [config.py](file:///home/edson/Documents/langchain/mba-ia-refactor-projects-skill/code-smells-project/config.py) pela adição do carregamento com `python-dotenv` e remoção do segredo em formato literal.
* **[C-2] God Class / Acoplamento no Entry Point:** As rotas administrativas `/admin/reset-db` e `/admin/query` foram extraídas de `app.py` para o blueprint [admin_routes.py](file:///home/edson/Documents/langchain/mba-ia-refactor-projects-skill/code-smells-project/routes/admin_routes.py) e o controlador [admin_controller.py](file:///home/edson/Documents/langchain/mba-ia-refactor-projects-skill/code-smells-project/controllers/admin_controller.py).
* **[H-1] Geração de Token JWT exposto diretamente em Rota:** A responsabilidade de gerar e assinar o JWT foi movida de [usuario_routes.py](file:///home/edson/Documents/langchain/mba-ia-refactor-projects-skill/code-smells-project/routes/usuario_routes.py) para o método `gerar_token` do [usuario_controller.py](file:///home/edson/Documents/langchain/mba-ia-refactor-projects-skill/code-smells-project/controllers/usuario_controller.py).
* **[M-1] Desvio de Camada em Middlewares (Bypass de Controller):** Modificado o decorator `token_required` em [auth_helper.py](file:///home/edson/Documents/langchain/mba-ia-refactor-projects-skill/code-smells-project/routes/auth_helper.py) para recuperar o usuário chamando o `usuario_controller.buscar_usuario` em vez de chamar diretamente o model.
* **[L-1] Código Morto / Duplicado e com Bug:** Arquivo redundante `routes/auth.py` removido e o blueprint `admin_routes.py` foi limpo de rotas duplicadas ou erros de passagem de parâmetros.

## 4. Desvios Encontrados (Itens não conformes)
*Nenhum desvio foi encontrado. O código refatorado respeita integralmente as diretrizes do padrão MVC e os requisitos técnicos.*

## 5. Conclusão e Próximos Passos
O projeto foi refatorado de forma exemplar. A separação de responsabilidades está nítida e os riscos de segurança apontados na auditoria anterior foram completamente sanados. O sistema está estável, operacional e pronto para produção.
