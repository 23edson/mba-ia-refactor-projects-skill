# Relatório de Auditoria — Projeto 3 (task-manager-api)

```
╔══════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE AUDITORIA ARQUITETURAL                ║
╚══════════════════════════════════════════════════════════════╝

Projeto:    task-manager-api
Stack:      Python + Flask
Data:       2026-07-11
Total de findings: 9

┌─────────────────────────────────────────────────────────────┐
│  CRITICAL: 3  │  HIGH: 3  │  MEDIUM: 1  │  LOW: 2  │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════
 🔴 CRITICAL
═══════════════════════════════════

[C-1] Credenciais SMTP Hardcoded (AP-02)
  Arquivo: services/notification_service.py:9-10
  Descrição: O e-mail e a senha do Gmail estão expostos diretamente no construtor da classe `NotificationService`.
  Código:
    self.email_user = 'taskmanager@gmail.com'
    self.email_password = 'senha123'
  Impacto: Comprometimento de credenciais em caso de vazamento ou exposição do código-fonte.
  Recomendação: Obter as configurações através de variáveis de ambiente (`os.getenv`).

[C-2] Credenciais Hardcoded / Secret Key (AP-02)
  Arquivo: app.py:13
  Descrição: A chave secreta do Flask está exposta diretamente no arquivo principal da aplicação.
  Código:
    app.config['SECRET_KEY'] = 'super-secret-key-123'
  Impacto: Permite que atacantes falsifiquem sessões e cookies, comprometendo a segurança da aplicação.
  Recomendação: Usar variável de ambiente para inicializar `SECRET_KEY`.

[C-3] Senhas em Texto Puro / Criptografia Fraca (AP-03)
  Arquivo: models/user.py:29-32
  Descrição: A senha está sendo armazenada e comparada usando o algoritmo hash MD5, que é inseguro e obsoleto.
  Código:
    self.password = hashlib.md5(pwd.encode()).hexdigest()
    return self.password == hashlib.md5(pwd.encode()).hexdigest()
  Impacto: Senhas vulneráveis a ataques de dicionário e força bruta devido à fragilidade do algoritmo MD5.
  Recomendação: Substituir MD5 por bcrypt.

═══════════════════════════════════
 🟠 HIGH
═══════════════════════════════════

[H-1] Lógica de Negócio em Controller/Route (AP-05)
  Arquivo: routes/task_routes.py:30-39
  Descrição: A verificação de se uma tarefa está atrasada está implementada diretamente no arquivo de rotas, misturando lógica de negócio com a de apresentação/roteamento.
  Código:
    if t.due_date:
        if t.due_date < datetime.utcnow():
            if t.status != 'done' and t.status != 'cancelled':
                task_data['overdue'] = True
  Impacto: Acoplamento de código, impedindo testes de unidade limpos e isolados.
  Recomendação: Utilizar o método `is_overdue()` do próprio model `Task` e encapsular em um controller.

[H-2] Lógica de Negócio em Controller/Route (AP-05)
  Arquivo: routes/user_routes.py:61-69
  Descrição: A validação de formato de e-mail e regras de tamanho mínimo da senha estão expostas na função de tratamento de rotas.
  Código:
    if not re.match(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', email):
        return jsonify({'error': 'Email inválido'}), 400
  Impacto: Dificuldade em reutilizar regras de validação em outros endpoints ou comandos.
  Recomendação: Centralizar a lógica de criação de usuário com validação em um controller de usuários.

[H-3] Sem Autenticação em Rotas Protegidas (AP-06)
  Arquivo: routes/report_routes.py:12
  Descrição: O endpoint de relatório `/reports/summary` não exige token de autenticação, permitindo acesso não autorizado.
  Código:
    @report_bp.route('/reports/summary', methods=['GET'])
    def summary_report():
  Impacto: Acesso irrestrito a dados estratégicos e estatísticas de produtividade dos usuários da aplicação.
  Recomendação: Implementar um middleware ou decorator de autenticação (JWT) e aplicá-lo nos endpoints de relatórios.

═══════════════════════════════════
 🟡 MEDIUM
═══════════════════════════════════

[M-1] N+1 Queries (AP-08)
  Arquivo: routes/task_routes.py:41-57
  Descrição: No endpoint `/tasks`, a aplicação faz uma query no banco de dados para buscar o usuário e outra para a categoria correspondente a cada tarefa em um loop `for`.
  Código:
    if t.user_id:
        user = User.query.get(t.user_id)
    ...
    if t.category_id:
        cat = Category.query.get(t.category_id)
  Impacto: Problemas severos de performance conforme o volume de tarefas cresce (2N + 1 queries).
  Recomendação: Realizar eager loading (join) ao consultar as tarefas (usando `joinedload` do SQLAlchemy).

═══════════════════════════════════
 🔵 LOW
═══════════════════════════════════

[L-1] Console/Print como Logging (AP-13)
  Arquivo: routes/user_routes.py:83
  Descrição: Utilização da função global `print()` para registrar eventos de criação e erros, em vez de um logger estruturado.
  Código:
    print(f"Usuário criado: {user.id} - {user.name}")
  Impacto: Falta de padronização, níveis de log, timestamps automáticos e incapacidade de redirecionar logs em ambiente de produção.
  Recomendação: Importar e utilizar o módulo `logging` padrão do Python.

[L-2] Código Não Utilizado / Imports Não Utilizados (AP-16)
  Arquivo: app.py:7
  Descrição: Importações desnecessárias de pacotes como `os`, `sys`, `json` no entry point.
  Código:
    import os, sys, json, datetime
  Impacto: Aumenta a poluição do código e dificulta a manutenção estática.
  Recomendação: Remover imports não utilizados e configurar regras de linting para evitar novos casos.

═══════════════════════════════════
 RESUMO DE AÇÕES NECESSÁRIAS
═══════════════════════════════════

CRITICAL (corrigir antes de qualquer deploy):
  - [ ] Mover as credenciais SMTP de `NotificationService` para variáveis de ambiente [C-1]
  - [ ] Mover a `SECRET_KEY` de `app.py` para variáveis de ambiente [C-2]
  - [ ] Substituir algoritmo MD5 de hash de senha de usuários por bcrypt [C-3]

HIGH (corrigir nesta sprint):
  - [ ] Reutilizar método `is_overdue()` do model `Task` e encapsular a lógica no controller [H-1]
  - [ ] Mover validação de dados de cadastro de rotas para o controller de usuário [H-2]
  - [ ] Proteger endpoints de relatórios com autenticação baseada em token [H-3]

MEDIUM (planejar para próxima sprint):
  - [ ] Otimizar listagem de tarefas com `joinedload` para evitar N+1 queries [M-1]

LOW (melhorias incrementais):
  - [ ] Substituir o uso de `print` por módulo `logging` estruturado [L-1]
  - [ ] Limpar importações não utilizadas de `app.py` e demais arquivos [L-2]
```
