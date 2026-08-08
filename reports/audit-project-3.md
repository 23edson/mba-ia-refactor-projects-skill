╔══════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE AUDITORIA ARQUITETURAL                ║
╚══════════════════════════════════════════════════════════════╝

Projeto:    task-manager-api
Stack:      Python + Flask 3.0.0 + Flask-SQLAlchemy
Data:       2026-08-08
Total de findings: 9

┌─────────────────────────────────────────────────────────────┐
│  CRITICAL: 0  │  HIGH: 2  │  MEDIUM: 3  │  LOW: 4          │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════
 🟠 HIGH
═══════════════════════════════════

[H-1] Token JWT Fake — Sem Autenticação Real (AP-06)
  Arquivo: utils/auth.py:14
  Descrição: O mecanismo de autenticação usa um token fictício previsível
  ("fake-jwt-token-<user_id>") sem assinatura criptográfica. Qualquer pessoa
  que saiba o ID de um usuário pode forjar um token válido.
  Código:
    user_id = int(token.replace('Bearer fake-jwt-token-', ''))
  Impacto: Permite que qualquer usuário forje tokens de outros usuários
  (inclusive admin), contornando toda a proteção de autenticação da API.
  Recomendação: Implementar JWT real com PyJWT, assinar com SECRET_KEY e
  verificar a assinatura antes de confiar no payload.

[H-2] Hard Delete de Categoria sem Verificação de Integridade (AP-11)
  Arquivo: controllers/category_controller.py:44-48
  Descrição: A função delete_category remove a categoria diretamente do banco
  sem verificar se existem tasks associadas a ela.
  Código:
    def delete_category(cat_id):
        cat = Category.query.get(cat_id)
        ...
        db.session.delete(cat)
        db.session.commit()
  Impacto: Tasks com category_id órfão podem causar inconsistência de dados
  e erros em listagens que fazem joinedload da categoria.
  Recomendação: Verificar Task.query.filter_by(category_id=cat_id).count()
  antes de deletar, ou usar ON DELETE SET NULL na FK / soft delete.

═══════════════════════════════════
 🟡 MEDIUM
═══════════════════════════════════

[M-1] Uso de Model.query.get() Deprecado (AP-15)
  Arquivo: controllers/task_controller.py:33, 63, 69, 100, 133, 141, 168
           controllers/user_controller.py:22, 63, 99, 111
           controllers/category_controller.py:28, 43
           controllers/report_controller.py:90
           utils/auth.py:15
  Descrição: O método Session.get() substituiu Model.query.get() no
  SQLAlchemy 2.x. O uso legado de .query.get() gera DeprecationWarning.
  Código:
    task = Task.query.get(task_id)
    user = User.query.get(user_id)
  Impacto: Quebra de compatibilidade em versões futuras do SQLAlchemy.
  Recomendação: Substituir por db.session.get(Task, task_id) em todos os
  arquivos afetados (15 ocorrências no total).

[M-2] Bare Except — Captura Silenciosa de Exceções (AP-10)
  Arquivo: utils/helpers.py:43, 46
           controllers/task_controller.py:85, 151
  Descrição: Uso de bloco `except:` sem especificar o tipo de exceção captura
  até KeyboardInterrupt e SystemExit, podendo mascarar erros críticos.
  Código:
    except:
        try:
            return datetime.strptime(date_string, '%d/%m/%Y')
        except:
            return None
  Impacto: Erros inesperados são silenciados, tornando o diagnóstico de
  problemas em produção extremamente difícil.
  Recomendação: Substituir `except:` por `except (ValueError, TypeError):` ou
  a exceção específica esperada.

[M-3] str(e) Exposto em Respostas da API (AP-10)
  Arquivo: routes/user_routes.py:26, 48, 65, 78, 90, 112
           routes/task_routes.py:26, 40, 56, 71
           routes/category_routes.py:34, 50, 62
           routes/report_routes.py:30
  Descrição: Erros de ValueError (que contêm mensagens de negócio do
  controller) são retornados diretamente ao cliente via str(e). Embora
  ValueError seja controlado neste projeto, o padrão é perigoso pois
  qualquer exceção não prevista também poderia ser exposta.
  Código:
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
  Impacto: Vaza detalhes internos do modelo de domínio ao cliente caso
  uma exceção inesperada seja capturada como ValueError.
  Recomendação: Para ValueError controlados (mensagens de negócio), o
  padrão é aceitável. Garantir que nenhum outro tipo de exceção chegue a
  este bloco adicionando um `except Exception` separado com mensagem genérica.

═══════════════════════════════════
 🔵 LOW
═══════════════════════════════════

[L-1] Funções Utilitárias Sem Uso (AP-16)
  Arquivo: utils/helpers.py:7, 12, 20, 23, 26, 29, 49, 52
  Descrição: As funções format_date, calculate_percentage, validate_email,
  sanitize_string, generate_id, is_valid_color e process_task_data estão
  definidas em helpers.py mas não são importadas ou chamadas em nenhum
  outro arquivo do projeto.
  Código:
    def generate_id():
        import uuid
        return str(uuid.uuid4())
  Impacto: Código morto aumenta a superfície de manutenção e confunde
  novos contribuidores sobre o que está realmente em uso.
  Recomendação: Remover as funções não utilizadas ou, se necessário para
  uso futuro, mover para um módulo utilitário claramente nomeado.

[L-2] type(tags) == list em vez de isinstance (AP-14)
  Arquivo: utils/helpers.py:100
  Descrição: A comparação de tipo usa type() == em vez do idiomático isinstance(),
  que é mais robusto e compatível com subclasses.
  Código:
    if type(tags) == list:
  Impacto: Falha silenciosa se tags for uma subclasse de list.
  Recomendação: Substituir por isinstance(tags, list).

[L-3] Senha Mínima de 4 Caracteres (AP-12)
  Arquivo: controllers/user_controller.py:36
           seed.py:22,27,32
  Descrição: A regra de negócio exige apenas 4 caracteres para a senha,
  e o seed usa senhas de 4 letras ('1234', 'abcd', 'pass').
  Código:
    if len(password) < 4:
        raise ValueError('Senha deve ter no mínimo 4 caracteres')
  Impacto: Vulnerabilidade a ataques de força bruta.
  Recomendação: Aumentar para mínimo de 8 caracteres e exigir complexidade
  (letras + números), mesmo em ambiente de desenvolvimento.

[L-4] Lógica Duplicada de Validação de Status e Prioridade (AP-09)
  Arquivo: controllers/task_controller.py:54, 58, 120, 126
           models/task.py:44, 49
  Descrição: As validações de status válidos e intervalo de prioridade estão
  implementadas tanto no controller quanto como métodos no model (validate_status,
  validate_priority), mas os métodos do model nunca são chamados.
  Código:
    # Em task_controller.py:54
    if status not in ['pending', 'in_progress', 'done', 'cancelled']:
    # Em models/task.py:44 (nunca chamado)
    def validate_status(self, new_status):
        valid = ['pending', 'in_progress', 'done', 'cancelled']
  Impacto: Inconsistência de manutenção — alterar a lista de status válidos
  exige atualizar dois lugares.
  Recomendação: Usar apenas os métodos do model ou centralizar as constantes
  em utils/helpers.py (VALID_STATUSES já está lá mas também não é usado).

═══════════════════════════════════
 RESUMO DE AÇÕES NECESSÁRIAS
═══════════════════════════════════

HIGH (corrigir nesta sprint):
  - [ ] [H-1] Implementar JWT real com PyJWT substituindo o fake-jwt-token.
  - [ ] [H-2] Verificar tasks associadas antes de deletar categoria.

MEDIUM (planejar para próxima sprint):
  - [ ] [M-1] Substituir Model.query.get() por db.session.get() em 15 ocorrências.
  - [ ] [M-2] Substituir bare `except:` por exceções específicas (4 ocorrências).
  - [ ] [M-3] Garantir que apenas ValueError de negócio é exposto via str(e).

LOW (melhorias incrementais):
  - [ ] [L-1] Remover ou usar as 7 funções utilitárias sem uso em helpers.py.
  - [ ] [L-2] Substituir type(tags) == list por isinstance(tags, list).
  - [ ] [L-3] Aumentar senha mínima de 4 para 8 caracteres.
  - [ ] [L-4] Centralizar validações de status/prioridade e remover duplicação.
