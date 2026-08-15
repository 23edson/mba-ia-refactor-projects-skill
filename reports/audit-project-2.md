╔══════════════════════════════════════════════════════════════╗
║           RELATÓRIO DE AUDITORIA ARQUITETURAL                ║
╚══════════════════════════════════════════════════════════════╝

Projeto:    ecommerce-api-legacy
Stack:      JavaScript/Node.js + Express
Data:       2026-08-15
Total de findings: 9

┌─────────────────────────────────────────────────────────────┐
│  CRITICAL: 3  │  HIGH: 2  │  MEDIUM: 2  │  LOW: 2  │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════
 🔴 CRITICAL
═══════════════════════════════════

[C-1] Credenciais Hardcoded (AP-02)
  Arquivo: src/utils.js:1-7
  Descrição: Credenciais confidenciais, incluindo senhas de banco de dados, chaves de API de pagamento e configurações SMTP, expostas diretamente no código-fonte.
  Código:
    const config = {
        dbUser: "admin_master",
        dbPass: "senha_super_secreta_prod_123", 
        paymentGatewayKey: "pk_live_1234567890abcdef",
        smtpUser: "no-reply@fullcycle.com.br",
        port: 3000
    };
  Impacto: Vazamento potencial de chaves secretas de infraestrutura e serviços de pagamento se o código-fonte for comprometido.
  Recomendação: Mover as configurações para variáveis de ambiente via arquivo `.env` e carregá-las no `config.js` usando `process.env`.

[C-2] Senhas em Texto Puro / Criptografia Ruim (AP-03)
  Arquivo: src/utils.js:17-23, src/AppManager.js:18
  Descrição: Uso de um algoritmo personalizado inseguro `badCrypto` baseado em conversões sucessivas para Base64 sem sal, além de armazenamento de senha do usuário inicial ("123") em texto puro no banco de dados.
  Código:
    function badCrypto(pwd) {
        let hash = "";
        for(let i = 0; i < 10000; i++) {
            hash += Buffer.from(pwd).toString('base64').substring(0, 2);
        }
        return hash.substring(0, 10);
    }
  Impacto: Ataques de força bruta e engenharia reversa de senhas facilitados em caso de comprometimento do banco de dados, além de exposição direta da senha inicial.
  Recomendação: Utilizar hashing seguro unidirecional com sal (ex: `bcrypt` ou `bcryptjs`) e remover a função `badCrypto`.

[C-3] God Class / Monolito (AP-04)
  Arquivo: src/AppManager.js:4-142
  Descrição: A classe `AppManager` atua como God Class, concentrando a conexão com o SQLite, inicialização das tabelas, definição de rotas e toda a lógica de negócio e validação no mesmo arquivo.
  Código:
    class AppManager {
        constructor() {
            this.db = new sqlite3.Database(':memory:');
        }
        initDb() { ... }
        setupRoutes(app) { ... }
    }
  Impacto: Alto acoplamento, impedindo testes unitários em isolamento e tornando a manutenção e escalabilidade extremamente complexas.
  Recomendação: Decompor a classe no padrão MVC: Models para acesso a dados, Controllers para lógica de negócio, e Routes para o roteamento.

═══════════════════════════════════
 🟠 HIGH
═══════════════════════════════════

[H-1] Sem Autenticação em Rotas Protegidas (AP-06)
  Arquivo: src/AppManager.js:80, src/AppManager.js:131
  Descrição: As rotas administrativas e destrutivas (`/api/admin/financial-report` e `/api/users/:id`) não possuem validação de autenticação ou autorização.
  Código:
    app.get('/api/admin/financial-report', (req, res) => { ... })
    app.delete('/api/users/:id', (req, res) => { ... })
  Impacto: Qualquer cliente/usuário não autenticado pode deletar usuários e visualizar relatórios financeiros confidenciais da aplicação.
  Recomendação: Implementar um middleware de autenticação (ex: JWT ou similar) para validar o token no cabeçalho Authorization das rotas protegidas.

[H-2] Sem Transação em Operações Compostas (AP-07)
  Arquivo: src/AppManager.js:50-63
  Descrição: Operação de checkout realiza inserções em sequência no banco de dados (`enrollments`, `payments` e `audit_logs`) sem usar transações de banco (BEGIN/COMMIT/ROLLBACK).
  Código:
    this.db.run("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", [userId, cid], function(err) {
        ...
        self.db.run("INSERT INTO payments (enrollment_id, amount, status) VALUES (?, ?, ?)", [enrId, course.price, status], function(err) { ... })
    })
  Impacto: Possibilidade de estados inconsistentes se a segunda ou terceira escrita falhar após o sucesso da primeira (ex: matrícula gerada sem registro de pagamento).
  Recomendação: Envolver o fluxo de inserção múltipla em uma transação (`BEGIN TRANSACTION`, `COMMIT` e `ROLLBACK` em caso de erro).

═══════════════════════════════════
 🟡 MEDIUM
═══════════════════════════════════

[M-1] N+1 Queries (AP-08)
  Arquivo: src/AppManager.js:89-127
  Descrição: A rota de relatório financeiro realiza uma query principal em `courses` e, em um loop `forEach`, faz novas queries na tabela `enrollments`, e dentro desta iteração, faz novas queries individuais em `users` e `payments`.
  Código:
    this.db.all("SELECT * FROM courses", [], (err, courses) => {
        ...
        courses.forEach(c => {
            ...
            this.db.all("SELECT * FROM enrollments WHERE course_id = ?", [c.id], (err, enrollments) => {
                ...
                enrollments.forEach(enr => {
                    this.db.get("SELECT name, email FROM users WHERE id = ?", ...)
                    this.db.get("SELECT amount, status FROM payments WHERE ...", ...)
  Impacto: Queda grave de performance com o aumento no volume de dados devido ao excesso de conexões e queries síncronas enviadas ao banco.
  Recomendação: Reestruturar o fluxo usando `JOIN` para trazer todas as informações relacionadas de uma única vez em uma única consulta.

[M-2] Hard Delete sem Verificação de Integridade (AP-11)
  Arquivo: src/AppManager.js:131-137
  Descrição: Deleção permanente (Hard Delete) de registros da tabela `users` sem verificar relacionamentos pendentes na tabela `enrollments`.
  Código:
    app.delete('/api/users/:id', (req, res) => {
        let id = req.params.id;
        this.db.run("DELETE FROM users WHERE id = ?", [id], (err) => { ... })
    })
  Impacto: Dados órfãos na tabela de matrículas e pagamentos, quebrando relatórios e causando erros de consistência de dados.
  Recomendação: Validar se existem matrículas ativas para o usuário antes de permitir a exclusão, ou implementar Soft Delete atualizando uma flag de status.

═══════════════════════════════════
 🔵 LOW
═══════════════════════════════════

[L-1] Nomenclatura Problemática (AP-14)
  Arquivo: src/AppManager.js:29-33
  Descrição: Declaração de variáveis locais com nomes compostos por caracteres únicos ou extremamente curtos (`u`, `e`, `p`, `cid`, `cc`) no escopo do checkout.
  Código:
    let u = req.body.usr;
    let e = req.body.eml;
    let p = req.body.pwd;
    let cid = req.body.c_id;
    let cc = req.body.card;
  Impacto: Dificuldade de legibilidade e aumento da carga cognitiva na manutenção do código.
  Recomendação: Utilizar nomes descritivos para variáveis locais (ex: `username`, `email`, `password`, `courseId`, `creditCard`).

[L-2] APIs Deprecated / Obsoletas (AP-15)
  Arquivo: src/utils.js:20
  Descrição: Uso do construtor de buffer legado/descontinuado `new Buffer(pwd)` para codificação Base64.
  Código:
    hash += Buffer.from(pwd).toString('base64').substring(0, 2);
  Impacto: Embora o trecho use `Buffer.from(pwd)`, a recomendação geral do ecossistema Node.js é evitar inteiramente construtores legados se eles existirem ou puden-se ser referenciados em outras partes do código.
  Recomendação: Garantir o uso estrito de `Buffer.from()` e `Buffer.alloc()`.

═══════════════════════════════════
 RESUMO DE AÇÕES NECESSÁRIAS
═══════════════════════════════════

CRITICAL (corrigir antes de qualquer deploy):
  - [ ] Mover segredos/configurações em `src/utils.js` para variáveis de ambiente `.env` carregadas via `config.js` [C-1]
  - [ ] Substituir o hashing personalizado `badCrypto` pelo uso de `bcryptjs` para senhas dos usuários [C-2]
  - [ ] Decompor a classe `AppManager` estruturando o projeto no padrão arquitetural MVC [C-3]

HIGH (corrigir nesta sprint):
  - [ ] Adicionar middleware de autenticação (JWT) para proteger a rota de relatório financeiro e deleção de usuário [H-1]
  - [ ] Implementar transação na inserção atômica de matrículas, pagamentos e logs no checkout [H-2]

MEDIUM (planejar para próxima sprint):
  - [ ] Reescrever a query de relatório financeiro usando INNER/LEFT JOIN para resolver N+1 queries [M-1]
  - [ ] Adicionar checagem de matrículas ativas ou usar flag ativo (soft delete) ao deletar um usuário [M-2]

LOW (melhorias incrementais):
  - [ ] Renomear variáveis curtas de checkout para nomes autoexplicativos [L-1]
  - [ ] Assegurar conformidade com APIs não-deprecated de Buffer [L-2]
