# Relatório de Auditoria — Projeto code-smells-project

╔══════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE AUDITORIA ARQUITETURAL                ║
╚══════════════════════════════════════════════════════════════╝

Projeto:    code-smells-project
Stack:      Python + Flask
Data:       2026-08-15
Total de findings: 5

┌─────────────────────────────────────────────────────────────┐
│  CRITICAL: 2  │  HIGH: 1  │  MEDIUM: 1  │  LOW: 1  │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════
 🔴 CRITICAL
═══════════════════════════════════

[C-1] Credenciais Hardcoded / Fallback Inseguro (AP-02)
  Arquivo: config.py:4
  Descrição: Fallback da SECRET_KEY hardcoded como "minha-chave-super-secreta-123" se a variável de ambiente não estiver definida.
  Código:
    SECRET_KEY = os.environ.get("SECRET_KEY", "minha-chave-super-secreta-123")
  Impacto: Se a variável de ambiente não for configurada no ambiente de deploy, a aplicação usará a chave padrão insegura, permitindo a falsificação de tokens JWT por atacantes.
  Recomendação: Remover o fallback estático e exigir que a variável `SECRET_KEY` esteja presente no ambiente, lançando um erro de inicialização em sua ausência.

[C-2] God Class / Acoplamento no Entry Point (AP-04)
  Arquivo: app.py:77-91 e app.py:96-115
  Descrição: O entry point `app.py` define endpoints administrativos que realizam queries brutas diretamente no banco de dados e processam lógica de negócio (reset de banco e execução de consultas genéricas).
  Código:
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
  Impacto: Aumenta a complexidade do arquivo de inicialização da aplicação, viola a separação de responsabilidades e impede testes isolados dessas funcionalidades administrativas.
  Recomendação: Extrair a lógica dessas ações para um controlador apropriado e registrá-las em rotas sob um blueprint dedicado (ex: `/admin`).

═══════════════════════════════════
 🟠 HIGH
═══════════════════════════════════

[H-1] Lógica de Negócio e Segurança em Rota (AP-05)
  Arquivo: routes/usuario_routes.py:35-44
  Descrição: O processo de geração e assinatura de tokens JWT está codificado diretamente no handler do endpoint de login.
  Código:
    payload = {
        "sub": usuario["id"],
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
  Impacto: A lógica de segurança está acoplada à rota HTTP de login, impedindo sua reutilização e dificultando a mudança de parâmetros de segurança globais.
  Recomendação: Mover a geração do token para um método utilitário ou controller de autenticação.

═══════════════════════════════════
 🟡 MEDIUM
═══════════════════════════════════

[M-1] Desvio de Camada em Middlewares / Guards (Bypass de Controller) (AP-17)
  Arquivo: routes/auth_helper.py:25
  Descrição: O middleware `token_required` importa e consulta diretamente o Model de usuário (`usuario_model`), ignorando a camada Controller.
  Código:
    usuario = usuario_model.get_usuario_por_id(db, usuario_id)
  Impacto: Acopla o middleware de rotas diretamente aos detalhes de persistência do Model, quebrando a hierarquia correta de chamadas do MVC.
  Recomendação: Modificar `routes/auth_helper.py` para usar `usuario_controller.buscar_usuario` passando a conexão ativa com o banco.

═══════════════════════════════════
 🔵 LOW
═══════════════════════════════════

[L-1] Código Morto / Duplicado e com Bug (AP-16)
  Arquivo: routes/auth.py e routes/admin_routes.py
  Descrição: Os arquivos `routes/auth.py` e `routes/admin_routes.py` estão duplicados, não são registrados na aplicação, e `auth.py` possui um bug na linha 21 ao chamar `buscar_usuario` sem passar `db`.
  Código:
    user = usuario_controller.buscar_usuario(user_id)
  Impacto: Polui o repositório com código não utilizado, aumenta o custo cognitivo de manutenção e introduz um erro de runtime caso fosse chamado.
  Recomendação: Remover ambos os arquivos, centralizando toda a lógica de proteção nas rotas oficiais que usam `routes/auth_helper.py`.

═══════════════════════════════════
 RESUMO DE AÇÕES NECESSÁRIAS
═══════════════════════════════════

CRITICAL (corrigir antes de qualquer deploy):
  - [ ] Ajustar `config.py` para lançar exceção se `SECRET_KEY` não for provida via `.env`.
  - [ ] Mover `/admin/reset-db` e `/admin/query` de `app.py` para controladores e rotas dedicadas.

HIGH (corrigir nesta sprint):
  - [ ] Extrair geração do JWT de `routes/usuario_routes.py` para um controlador/serviço.

MEDIUM (planejar para próxima sprint):
  - [ ] Substituir o bypass do model em `routes/auth_helper.py` para chamar o `usuario_controller`.

LOW (melhorias incrementais):
  - [ ] Excluir os arquivos obsoletos `routes/auth.py` e `routes/admin_routes.py`.
