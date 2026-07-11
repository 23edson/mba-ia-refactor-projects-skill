╔══════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE AUDITORIA ARQUITETURAL                ║
╚══════════════════════════════════════════════════════════════╝

Projeto:    code-smells-project
Stack:      Python + Flask
Data:       2026-07-11
Total de findings: 15

┌─────────────────────────────────────────────────────────────┐
│  CRITICAL: 4  │  HIGH: 3  │  MEDIUM: 4  │  LOW: 4  │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════
 🔴 CRITICAL
═══════════════════════════════════

[C-1] SQL Injection (AP-01)
  Arquivo: models.py:28
  Descrição: Queries SQL construídas por concatenação de strings com parâmetros de entrada diretamente (presente em quase todas as queries do models.py).
  Código:
    cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
  Impacto: Permite que um atacante execute queries arbitrárias, podendo ler dados confidenciais ou apagar o banco de dados.
  Recomendação: Substituir a concatenação por queries parametrizadas com placeholders `?` e passar os valores como tupla.

[C-2] SQL Injection - Execução de SQL Arbitrário (AP-01)
  Arquivo: app.py:68
  Descrição: Rota /admin/query permite a execução de qualquer string SQL enviada no corpo da requisição diretamente no banco de dados.
  Código:
    cursor.execute(query)
  Impacto: Um atacante externo com acesso a essa rota pode executar qualquer instrução SQL (como DROP TABLE) e obter controle total do banco.
  Recomendação: Remover este endpoint inteiramente ou limitá-lo estritamente a fins administrativos seguros (autenticados e sem SQL livre).

[C-3] Credenciais Hardcoded (AP-02)
  Arquivo: app.py:7
  Descrição: Chave secreta de sessão da aplicação Flask exposta diretamente no código-fonte, e também exposta na resposta do endpoint /health.
  Código:
    app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
  Impacto: Permite que atacantes forjem cookies de sessão válidos da aplicação, comprometendo a autenticação global de usuários.
  Recomendação: Mover a chave secreta para variáveis de ambiente e carregá-la usando `os.environ.get("SECRET_KEY")`. Omitir a chave da resposta do healthcheck.

[C-4] Senhas em Texto Puro (AP-03)
  Arquivo: models.py:109
  Descrição: Senhas dos usuários são salvas e comparadas em texto puro diretamente no banco de dados. Senhas também são expostas na listagem/busca de usuários.
  Código:
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = '" + email + "' AND senha = '" + senha + "'"
    )
  Impacto: Se o banco de dados for exposto, todas as senhas de usuários estarão visíveis imediatamente.
  Recomendação: Usar uma biblioteca de hashing (como bcrypt ou werkzeug.security) para gerar hashes de senha no cadastro e verificar no login. Omitir o campo senha das respostas da API.

═══════════════════════════════════
 🟠 HIGH
═══════════════════════════════════

[H-1] Lógica de Negócio em Controller/Route (AP-05)
  Arquivo: controllers.py:208
  Descrição: O controller de criação de pedidos lida diretamente com simulações de envio de e-mail, SMS e notificações push.
  Código:
    print("ENVIANDO EMAIL: Pedido " + str(resultado["pedido_id"]) + " criado...")
    print("ENVIANDO SMS: Seu pedido foi recebido!")
  Impacto: Aumenta o acoplamento do controller com canais de notificação específicos e dificulta testes automatizados da lógica de negócio de pedidos.
  Recomendação: Mover o fluxo de notificações para uma camada de serviço dedicada ou acionar via eventos após salvar o pedido.

[H-2] Sem Autenticação em Rotas Protegidas (AP-06)
  Arquivo: app.py:47
  Descrição: Rotas sensíveis e administrativas (como /admin/reset-db, /admin/query, /relatorios/vendas, /usuarios) estão expostas publicamente sem validação de permissão.
  Código:
    @app.route("/admin/reset-db", methods=["POST"])
    def reset_database():
  Impacto: Qualquer cliente da API pode redefinir o banco de dados inteiro ou acessar dados confidenciais dos usuários e vendas.
  Recomendação: Implementar um sistema de autenticação (ex: JWT ou Session-based) com controle de acesso baseado em roles (ex: apenas administradores acessam rotas com prefixo /admin).

[H-3] Sem Transação em Operações Compostas (AP-07)
  Arquivo: models.py:133
  Descrição: A função de criar pedido realiza múltiplos SELECTs, INSERTs (em tabelas de pedidos e itens) e UPDATEs (redução de estoque) sem controle transacional explícito.
  Código:
    def criar_pedido(usuario_id, itens):
        ...
        db.commit()
  Impacto: Em caso de falha no meio do processo (ex: erro ao inserir item de pedido), o banco de dados pode ficar em estado inconsistente (ex: estoque reduzido sem item de pedido correspondente).
  Recomendação: Utilizar bloco try/except abrangendo a operação de escrita de dados com `db.rollback()` no bloco except para garantir atomicidade.

═══════════════════════════════════
 🟡 MEDIUM
═══════════════════════════════════

[M-1] N+1 Queries (AP-08)
  Arquivo: models.py:188
  Descrição: Na listagem de pedidos, executa-se uma query no loop para obter os itens de cada pedido, e mais uma query dentro do sub-loop para obter o nome do produto.
  Código:
    for row in rows:
        ...
        cursor2.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(row["id"]))
  Impacto: A performance decai drasticamente conforme a quantidade de pedidos no banco de dados cresce, gerando centenas de chamadas desnecessárias.
  Recomendação: Utilizar JOINs de SQL para trazer os pedidos, seus itens e nomes dos produtos em uma única query combinada ou em queries batch bem limitadas.

[M-2] Validação Duplicada ou Incompleta entre Camadas (AP-09)
  Arquivo: controllers.py:43
  Descrição: Regras de validação (como preço/estoque negativos ou categorias válidas) estão presentes no controller mas ausentes no model.
  Código:
    if preco < 0:
        return jsonify({"erro": "Preço não pode ser negativo"}), 400
  Impacto: Permite inserção de dados inconsistentes caso o model seja invocado por outras vias sem passar pelo controller.
  Recomendação: Centralizar as regras de validação de negócios em modelos ou em uma camada de serviço compartilhada.

[M-3] Erro Interno Exposto ao Cliente (AP-10)
  Arquivo: controllers.py:12
  Descrição: Captura genérica de exceções no controller expõe a mensagem exata do erro interno ao cliente da API.
  Código:
    except Exception as e:
        print("ERRO: " + str(e))
        return jsonify({"erro": str(e)}), 500
  Impacto: Vaza informações sobre a estrutura interna da aplicação (ex: estrutura de tabelas, nomes de variáveis, stack traces do banco).
  Recomendação: Logar a exceção detalhadamente no servidor e retornar uma mensagem genérica amigável ao cliente final (ex: "Erro interno no servidor").

[M-4] Hard Delete sem Verificação de Integridade (AP-11)
  Arquivo: models.py:68
  Descrição: O produto é deletado diretamente do banco por meio de DELETE físico sem verificar se está associado a algum pedido existente.
  Código:
    cursor.execute("DELETE FROM produtos WHERE id = " + str(id))
  Impacto: Ocorre quebra de integridade referencial ou erros na consulta de pedidos históricos associados ao produto excluído.
  Recomendação: Impedir a exclusão caso o produto tenha pedidos associados, ou utilizar soft delete (coluna `ativo = 0`).

═══════════════════════════════════
 🔵 LOW
═══════════════════════════════════

[L-1] Magic Numbers (AP-12)
  Arquivo: models.py:257
  Descrição: Regras de descontos sobre faturamento bruto utilizam valores mágicos sem explicação contextual.
  Código:
    if faturamento > 10000:
        desconto = faturamento * 0.1
  Impacto: Torna a manutenção de regras comerciais complexa caso os limiares ou as porcentagens sofram alterações recorrentes.
  Recomendação: Definir constantes nomeadas claras para os limiares e taxas de desconto no topo do arquivo ou em um arquivo de configurações.

[L-2] Console/Print como Logging (AP-13)
  Arquivo: controllers.py:8
  Descrição: Uso direto de print() para logs de depuração e fluxos de negócio.
  Código:
    print("Listando " + str(len(produtos)) + " produtos")
  Impacto: Falta de estrutura nos logs, sem timestamp ou nível de severidade (INFO, ERROR, DEBUG), dificultando auditoria futura em ambientes de produção.
  Recomendação: Configurar e utilizar a biblioteca padrão `logging` do Python.

[L-3] Shadowing de Built-ins (AP-14)
  Arquivo: models.py:24
  Descrição: O parâmetro do método de busca de produto por ID se chama `id`, ocultando a função built-in do Python `id()`.
  Código:
    def get_produto_por_id(id):
  Impacto: Pode introduzir bugs sutis se o programador tentar invocar a função built-in `id()` no mesmo escopo.
  Recomendação: Renomear o parâmetro para `produto_id` ou `id_`.

[L-4] Código Não Utilizado / Imports Mortos (AP-16)
  Arquivo: controllers.py:3
  Descrição: Importação de get_db do módulo database sem qualquer utilização nas funções do arquivo.
  Código:
    from database import get_db
  Impacto: Poluição visual do código e desperdício de recursos/importação.
  Recomendação: Remover as importações e variáveis declaradas que não são referenciadas no código.

═══════════════════════════════════
 RESUMO DE AÇÕES NECESSÁRIAS
═══════════════════════════════════

CRITICAL (corrigir antes de qualquer deploy):
  - [ ] Parametrizar todas as queries SQL em `models.py` para evitar SQL Injection (C-1).
  - [ ] Remover a rota de execução de query SQL livre `/admin/query` ou restringi-la de forma segura e autenticada (C-2).
  - [ ] Transferir o segredo da aplicação para variáveis de ambiente e omiti-lo da rota de saúde (C-3).
  - [ ] Implementar criptografia de senhas com hashing (bcrypt) no cadastro/login e omitir senhas nas respostas HTTP (C-4).

HIGH (corrigir nesta sprint):
  - [ ] Mover lógica de notificação do controller para um fluxo de serviço isolado (H-1).
  - [ ] Criar middleware/funções de autenticação e proteção de rotas administrativas/sensíveis (H-2).
  - [ ] Implementar blocos de transação SQL e rollback em operações de múltiplos inserts/updates no banco (H-3).

MEDIUM (planejar para próxima sprint):
  - [ ] Otimizar as buscas de pedidos reduzindo as queries N+1 utilizando JOINs (M-1).
  - [ ] Sincronizar e organizar regras de validação nos models para manter consistência (M-2).
  - [ ] Modificar tratamento de erros nos controllers para não expor stack traces/erros crus da linguagem (M-3).
  - [ ] Implementar restrição ou soft delete ao deletar produtos para manter integridade das chaves estrangeiras (M-4).

LOW (melhorias incrementais):
  - [ ] Substituir valores mágicos comerciais por constantes declarativas nomeadas (L-1).
  - [ ] Trocar prints simples por logging estruturado do Python (L-2).
  - [ ] Corrigir nomes de parâmetros para evitar sombreamento de palavras reservadas da linguagem (L-3).
  - [ ] Limpar imports não utilizados nos cabeçalhos dos arquivos (L-4).
