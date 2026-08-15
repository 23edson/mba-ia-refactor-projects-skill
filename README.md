# Criação de Skills — Refatoração Arquitetural Automatizada

Ao longo do curso você aprendeu o que são Skills e como elas permitem que um agente de IA atue como um especialista em tarefas específicas. Agora imagine o seguinte cenário: você herdou 3 projetos legados com problemas de arquitetura, segurança e qualidade de código. Revisar e corrigir tudo manualmente levaria dias.

Neste desafio, você vai criar uma Skill que automatiza esse processo — analisando, auditando e refatorando qualquer projeto para o padrão MVC, independente da tecnologia.

## Objetivo

Você deve entregar uma Skill capaz de:

- Analisar uma codebase detectando linguagem, framework e arquitetura atual
- Identificar anti-patterns e code smells, classificando por severidade com arquivo e linha exatos
- Gerar um relatório de auditoria estruturado com todos os achados
- Refatorar o projeto para o padrão MVC (Model-View-Controller), eliminando os problemas encontrados
- Validar o resultado garantindo que a aplicação continua funcionando após as mudanças

A skill deve ser agnóstica de tecnologia, funcionando com diferentes linguagens e frameworks.

## Contexto

### Definição de Severidades

Para padronizar a sua auditoria e os relatórios gerados pela IA, utilize a seguinte escala de classificação baseada em problemas de MVC e SOLID:

- **CRITICAL:** Falhas graves de arquitetura ou segurança que impedem o funcionamento correto, expõem dados sensíveis (ex: credenciais hardcoded, SQL Injection) ou violam completamente a separação de responsabilidades (ex: "God Class" contendo banco de dados, lógicas complexas e roteamento no mesmo arquivo).
- **HIGH:** Fortes violações do padrão MVC ou princípios SOLID que dificultam muito a manutenção e testes (ex: lógicas de negócio pesadas presas dentro de Controllers, forte acoplamento sem Injeção de Dependência, ou uso de estado global mutável em toda a aplicação).
- **MEDIUM:** Problemas de padronização, duplicação de código ou gargalos de performance moderada (ex: Queries N+1 no banco de dados, uso inadequado de middlewares, validações ausentes nas rotas).
- **LOW:** Melhorias de legibilidade, nomenclatura de variáveis ruins, ou "magic numbers" soltos pelo código.

### Exemplo de Uso no CLI

```bash
# Executar a skill no projeto com problemas
cd code-smells-project
claude "/refactor-arch"
```

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      Python
Framework:      Flask 3.1.1
Dependencies:  flask-cors
Domain:        E-commerce API (produtos, pedidos, usuários)
Architecture:  Monolítica — tudo em 4 arquivos, sem separação de camadas
Source files:  4 files analyzed
DB tables:     produtos, usuarios, pedidos, itens_pedido
================================
```

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: code-smells-project
Stack:   Python + Flask
Files:   4 analyzed | ~800 lines of code

## Summary
CRITICAL: 4 | HIGH: 5 | MEDIUM: 2 | LOW: 3

## Findings

### [CRITICAL] God Class / God Method
File: models.py:1-350
Description: Arquivo único contém toda lógica de negócio, queries SQL, validação e formatação para 4 domínios diferentes.
Impact: Impossível testar em isolamento, qualquer mudança afeta tudo.
Recommendation: Separar em models e controllers por domínio.

### [CRITICAL] Hardcoded Credentials
File: app.py:8
Description: SECRET_KEY hardcoded como 'minha-chave-super-secreta-123'
...

================================
Total: 14 findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```

```
[... refatoração executada ...]

================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
src/
├── config/settings.py
├── models/
│   ├── produto_model.py
│   └── usuario_model.py
├── views/
│   └── routes.py
├── controllers/
│   ├── produto_controller.py
│   └── pedido_controller.py
├── middlewares/error_handler.py
└── app.py (composition root)

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

## Tecnologias obrigatórias

- **Ferramenta:** uma das três opções abaixo (não são aceitas outras ferramentas):
  - Claude Code
  - Gemini CLI
  - OpenAI Codex
- **Recurso:** Custom Skills (ou o equivalente na ferramenta escolhida)
- **Formato dos arquivos de referência:** Markdown
- **Projetos-alvo:** Python/Flask (2 projetos) e Node.js/Express (1 projeto) (fornecidos no repositório base)

> **Nota sobre a ferramenta:** Os exemplos deste documento usam o Claude Code (`.claude/skills/`) como referência, pois é a ferramenta utilizada no curso. Se você optar por Gemini CLI ou Codex, adapte o nome da pasta e o comando de invocação conforme a convenção dela — o conceito de skill e a estrutura interna (SKILL.md + arquivos de referência) permanecem os mesmos.

## Requisitos

### 1. Análise Manual dos Projetos

Antes de criar a skill, você deve entender os problemas que ela vai resolver.

**Tarefas:**

- Analisar o projeto `code-smells-project/` (Python/Flask — API de E-commerce)
- Analisar o projeto `ecommerce-api-legacy/` (Node.js/Express — LMS API com fluxo de checkout)
- Analisar o projeto `task-manager-api/` (Python/Flask — API de Task Manager)

Para cada projeto, identificar e documentar no mínimo 5 problemas, incluindo pelo menos:

- 1 de severidade CRITICAL ou HIGH
- 2 de severidade MEDIUM
- 2 de severidade LOW

Documentar os achados na seção "Análise Manual" do seu `README.md`

> **Dica:** Não precisa encontrar todos os problemas — foque nos que têm maior impacto arquitetural. Use os projetos como insumo para entender quais padrões sua skill precisa detectar.

> **Por que 3 projetos?** Dois são Python/Flask (com níveis de organização diferentes) e um é Node.js/Express. Sua skill precisa funcionar nos 3 para provar que é verdadeiramente agnóstica de tecnologia — lidando tanto com código completamente desestruturado quanto com projetos que já possuem alguma separação de camadas.

### 2. Criação da Skill

Agora que você conhece os problemas, crie uma skill que os detecte, gere um relatório de auditoria e corrija automaticamente.

**Tarefas:**

Criar a skill dentro do projeto `code-smells-project/` e implementar o SKILL.md com 3 fases sequenciais:

- **Fase 1 — Análise:** Detectar stack, mapear arquitetura atual, imprimir resumo
- **Fase 2 — Auditoria:** Cruzar código contra catálogo de anti-patterns, gerar relatório, pedir confirmação
- **Fase 3 — Refatoração:** Reestruturar para o padrão MVC, validar que funciona

Criar arquivos de referência em Markdown que forneçam à skill o conhecimento necessário para executar as 3 fases. Os arquivos devem cobrir **obrigatoriamente** as seguintes áreas de conhecimento:

| Área de conhecimento | O que deve conter |
|---|---|
| Análise de projeto | Heurísticas para detecção de linguagem, framework, banco de dados e mapeamento de arquitetura |
| Catálogo de anti-patterns | Anti-patterns com sinais de detecção e classificação de severidade |
| Template de relatório | Formato padronizado do relatório de auditoria (Fase 2) |
| Guidelines de arquitetura | Regras do padrão MVC alvo (camadas Models, Views/Routes e Controllers, responsabilidades de cada uma) |
| Playbook de refatoração | Padrões concretos de transformação para cada anti-pattern (com exemplos de código) |

> **Nota:** Você tem liberdade para organizar os arquivos de referência como preferir — pode usar os nomes e a quantidade de arquivos que fizer sentido para sua skill. O importante é que todas as 5 áreas de conhecimento estejam cobertas. O nome da skill (`refactor-arch`) e o arquivo `SKILL.md` são obrigatórios e não devem ser alterados. O path da skill segue a convenção da ferramenta escolhida (no Claude Code, por exemplo, é `.claude/skills/refactor-arch/`).

**Requisitos da skill:**

- Deve ser agnóstica de tecnologia — deve funcionar corretamente nos 3 projetos fornecidos, independente da stack ou nível de organização
- O catálogo de anti-patterns deve conter no mínimo 8 anti-patterns com severidade distribuída (CRITICAL, HIGH, MEDIUM, LOW)
- O catálogo deve incluir detecção de APIs deprecated — identificar uso de APIs obsoletas e recomendar o equivalente moderno
- O playbook deve ter no mínimo 8 padrões de transformação com exemplos de código antes/depois
- A Fase 2 deve pausar e pedir confirmação antes de modificar qualquer arquivo
- A Fase 3 deve validar o resultado (boot da aplicação + endpoints funcionando)

### 3. Execução da Skill

Execute sua skill nos 3 projetos e valide que ela funciona em todas as stacks.

#### Projeto 1 — code-smells-project (Python/Flask)

Invocar a skill no Claude Code:

```bash
claude "/refactor-arch"
```

> **Nota:** O comando acima é o exemplo com Claude Code. Se você estiver usando Gemini CLI ou Codex, utilize o comando equivalente para invocar uma skill na sua ferramenta.

- Verificar que a Fase 1 detecta corretamente a stack e imprime o resumo
- Verificar que a Fase 2 encontra no mínimo 5 dos problemas documentados na sua análise manual
- Confirmar a execução da Fase 3
- Verificar que a Fase 3:
  - Cria a estrutura de diretórios baseada em MVC
  - A aplicação inicia sem erros
  - Os endpoints originais continuam respondendo
- Salvar o relatório de auditoria (output da Fase 2) em `reports/audit-project-1.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 2 — ecommerce-api-legacy (Node.js/Express)

Prove que sua skill é reutilizável em outro projeto de backend, mas com stack diferente.

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `ecommerce-api-legacy/`
- Invocar a skill:

```bash
cd ../ecommerce-api-legacy
claude "/refactor-arch"
```

- Verificar que as 3 fases executam corretamente neste projeto
- Salvar o relatório em `reports/audit-project-2.md`
- Commitar o código refatorado do projeto no repositório

#### Projeto 3 — task-manager-api (Python/Flask)

Agora o teste com um projeto Python/Flask que já possui alguma organização de camadas (models, routes, services, utils).

- Copiar a pasta `.claude/skills/refactor-arch/` para dentro de `task-manager-api/`
- Invocar a skill:

```bash
cd ../task-manager-api
claude "/refactor-arch"
```

- Verificar que:
  - A Fase 1 detecta corretamente Python/Flask como stack e identifica o domínio de Task Manager
  - A Fase 2 identifica problemas mesmo em um projeto parcialmente organizado
  - A Fase 3 melhora a estrutura sem quebrar a aplicação (todos os endpoints devem continuar respondendo)
- Salvar o relatório em `reports/audit-project-3.md`
- Commitar o código refatorado do projeto no repositório

> **Nota:** Este projeto já possui alguma separação de camadas, mas isso não significa que a arquitetura está adequada. A skill deve identificar tanto problemas de código (segurança, performance, qualidade) quanto oportunidades de melhoria arquitetural. Se houver mudanças estruturais necessárias, a skill deve propô-las e executá-las.

#### Validação

Para cada projeto refatorado, valide o seguinte checklist:

```markdown
## Checklist de Validação

### Fase 1 — Análise
- [ ] Linguagem detectada corretamente
- [ ] Framework detectado corretamente
- [ ] Domínio da aplicação descrito corretamente
- [ ] Número de arquivos analisados condiz com a realidade

### Fase 2 — Auditoria
- [ ] Relatório segue o template definido nos arquivos de referência
- [ ] Cada finding tem arquivo e linhas exatos
- [ ] Findings ordenados por severidade (CRITICAL → LOW)
- [ ] Mínimo de 5 findings identificados
- [ ] Detecção de APIs deprecated incluída (se aplicável)
- [ ] Skill pausa e pede confirmação antes da Fase 3

### Fase 3 — Refatoração
- [ ] Estrutura de diretórios segue padrão MVC
- [ ] Configuração extraída para módulo de config (sem hardcoded)
- [ ] Models criados para abstrair dados
- [ ] Views/Routes separadas para visualização ou roteamento
- [ ] Controllers concentram o fluxo da aplicação
- [ ] Error handling centralizado
- [ ] Entry point claro
- [ ] Aplicação inicia sem erros
- [ ] Endpoints originais respondem corretamente
```

> **Dica:** Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Entregável

Repositório público no GitHub (fork do repositório base) contendo:

- Skill completa em `.claude/skills/refactor-arch/` (dentro dos 3 projetos)
- Código refatorado dos 3 projetos (resultado da execução da Fase 3, commitado no repositório)
- Relatórios de auditoria em `reports/` (3 arquivos)
- `README.md` atualizado

### Estrutura do repositório

Faça um fork do repositório base contendo os três projetos com code smells.

> **Nota:** A estrutura abaixo usa Claude Code como exemplo (`.claude/skills/`). Se estiver usando outra ferramenta, adapte os caminhos conforme a convenção dela.

```
desafio-skills/
├── README.md                              # Sua documentação
│
├── code-smells-project/                   # Projeto 1 — Python/Flask (API de E-commerce)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← SUA SKILL AQUI
│   │           ├── SKILL.md
│   │           └── (arquivos de referência)
│   ├── app.py
│   ├── controllers.py
│   ├── models.py
│   ├── database.py
│   └── requirements.txt
│
├── ecommerce-api-legacy/                  # Projeto 2 — Node.js/Express (LMS API com checkout)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── src/
│   │   ├── app.js
│   │   ├── AppManager.js
│   │   └── utils.js
│   ├── api.http
│   └── package.json
│
├── task-manager-api/                      # Projeto 3 — Python/Flask (API de Task Manager)
│   ├── .claude/
│   │   └── skills/
│   │       └── refactor-arch/             # ← CÓPIA DA SKILL
│   │           └── ...
│   ├── app.py
│   ├── database.py
│   ├── seed.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
│
└── reports/                               # Relatórios gerados
    ├── audit-project-1.md                 # Saída da Fase 2 no projeto 1
    ├── audit-project-2.md                 # Saída da Fase 2 no projeto 2
    └── audit-project-3.md                 # Saída da Fase 2 no projeto 3
```

**O que você vai criar:**

- `.claude/skills/refactor-arch/` — A skill completa (SKILL.md + arquivos de referência)
- Código refatorado dos 3 projetos — resultado da execução da Fase 3, commitado no repositório
- `reports/audit-project-{1,2,3}.md` — Relatório de auditoria de cada projeto
- `README.md` — Documentação do seu processo

**O que já vem pronto:**

- `code-smells-project/` — API de E-commerce Python/Flask com code smells intencionais
- `ecommerce-api-legacy/` — LMS API Node.js/Express (com fluxo de checkout) e problemas de implementação
- `task-manager-api/` — API de Task Manager Python/Flask com organização parcial e problemas de segurança/qualidade

> **Dica:** Cada projeto contém problemas intencionais de diferentes severidades (CRITICAL, HIGH, MEDIUM, LOW), incluindo falhas de segurança, violações arquiteturais e problemas de qualidade de código. Parte do desafio é identificá-los por conta própria através da análise manual do código.

### README.md deve conter

**A) Seção "Análise Manual":**

- Lista dos problemas identificados manualmente em cada projeto
- Classificação por severidade
- Justificativa de por que cada problema é relevante

**B) Seção "Construção da Skill":**

- Decisões de design: como estruturou o SKILL.md e os arquivos de referência
- Quais anti-patterns incluiu no catálogo e por quê
- Como garantiu que a skill é agnóstica de tecnologia
- Desafios encontrados e como resolveu

**C) Seção "Resultados":**

- Resumo dos relatórios de auditoria dos 3 projetos (quantos findings por severidade em cada)
- Comparação antes/depois da estrutura de cada projeto
- Checklist de validação preenchido para cada projeto
- Screenshots ou logs mostrando as aplicações rodando após refatoração
- Observações sobre como a skill se comportou em stacks diferentes

**D) Seção "Como Executar":**

- Pré-requisitos (a ferramenta escolhida — Claude Code, Gemini CLI ou Codex — instalada e configurada)
- Comandos para executar a skill em cada projeto
- Como validar que a refatoração funcionou

### Ordem de execução sugerida

**1. Analisar os projetos manualmente**

Leia o código dos três projetos e documente os problemas encontrados.

**2. Criar a skill**

Escreva o SKILL.md e os arquivos de referência.

**3. Executar nos 3 projetos**

```bash
# Projeto 1
cd code-smells-project
claude "/refactor-arch"

# Projeto 2
cd ../ecommerce-api-legacy
claude "/refactor-arch"

# Projeto 3
cd ../task-manager-api
claude "/refactor-arch"
```

Salve a saída da Fase 2 de cada projeto em `reports/audit-project-{1,2,3}.md`.

**4. Iterar**

Se a skill não detectou problemas suficientes ou a refatoração falhou, ajuste os arquivos de referência e execute novamente. É normal precisar de 2-4 iterações.

## Critérios de Aceite

A skill deve atingir os seguintes mínimos em **todos os 3 projetos**:

| Critério | Requisito |
|---|---|
| Fase 1 detecta stack corretamente | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 encontra >= 5 findings | OBRIGATÓRIO (3/3 projetos) |
| Fase 2 inclui pelo menos 1 CRITICAL ou HIGH | OBRIGATÓRIO (3/3 projetos) |
| Fase 3 aplicação funciona após refatoração | OBRIGATÓRIO (3/3 projetos) |

**IMPORTANTE:** Todos os critérios devem ser atingidos nos 3 projetos, não apenas em um!

> **Sobre o projeto 3 (task-manager-api):** Este projeto já possui alguma organização. "aplicação funciona" significa que a API inicia sem erros e todos os endpoints continuam respondendo corretamente.

## Referências

- [Claude Code: Skills](https://docs.anthropic.com/en/docs/claude-code/skills) — Documentação oficial sobre como criar e estruturar Skills
- [Claude Code: Overview](https://docs.anthropic.com/en/docs/claude-code/overview) — Visão geral do Claude Code e suas capacidades
- [The Complete Guide to Building Skills for Claude (PDF)](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) — Guia completo da Anthropic sobre construção de Skills
- [Equipping Agents for the Real World with Agent Skills](https://claude.com/blog/equipping-agents-for-the-real-world-with-agent-skills) — Blog oficial da Anthropic sobre Agent Skills

---

## Dicas Finais

- **Comece pela análise manual** — entender os problemas profundamente é essencial para criar uma skill que os detecte.
- **O SKILL.md é um prompt** — ele instrui o agente sobre o que fazer, enquanto os arquivos de referência fornecem o conhecimento de domínio.
- **Seja específico nos sinais de detecção** — "código ruim" não ajuda; "query SQL dentro de loop for" é acionável.
- **Teste incrementalmente** — não tente criar a skill perfeita de primeira.
- **A skill deve ser copiável** — se ela só funciona em um projeto específico, está acoplada demais. Teste nos 3 projetos para validar.
- **Projetos diferentes exigem adaptação** — a Fase 3 de um projeto já parcialmente organizado não vai ter as mesmas transformações de um monolito. Sua skill deve se adaptar ao contexto.
- **Pedir confirmação na Fase 2 é obrigatório** — o humano deve revisar o relatório antes de qualquer modificação.
- **Consulte as referências do curso** — revise a documentação oficial da ferramenta escolhida e os materiais das aulas para relembrar a estrutura e anatomia de uma skill.

---

# Documentação de Execução do Desafio

# Análise Manual: code-smells-project (Python/Flask)

## Problemas Identificados

### 1. SQL Injection (CRITICAL) - [Problema de segurança]
- **Arquivo**: `models.py`
- **Descrição**: Neste arquivo é feito o uso de concatenação de strings em queries SQL, ao invés de queries parametrizadas. Isso permitindo execução de comandos arbitrários, expondo o sistema a ataques de SQL Injection.
- **Exemplo**: 
    1. ```  
        cursor.execute("SELECT * FROM usuarios WHERE id = " + str(id)) // Valor de id pode manipular a query  
        
        ```
    
    2. ``` 
        cursor.execute("SELECT * FROM usuarios WHERE email = '" + email + "' AND senha = '" + senha + "'") // email e senha podem conter ' OR 1=1 -- -'
    

### 2. Lógica de Negócio Misturada com Acesso a Dados (MEDIUM) - [Problema de separação de responsabilidades]
- **Arquivo**: `models.py`
- **Descrição**: A função `relatorio_vendas` calcula regras de desconto
  diretamente junto às queries SQL:
   ```
      def relatorio_vendas():
        # ... queries SQL ...
        
        #logica de negócio
        if faturamento > 10000:
            desconto = faturamento * 0.1
        elif faturamento > 5000:
            desconto = faturamento * 0.05
    ```
  Na função `criar_pedido`, é feito validação de estoque
  e cálculo totais no mesmo nível do repositório.
  Isso mostra violação de separação de resposabilidade, dificulta criação de testes de unidade e reuso da regra de negócio.


### 3. Tratamento de Erros Inconsistente (MEDIUM) - [Problema de tratamento de erros/segurança]
- **Arquivo**: `controllers.py`
- **Descrição**: Blocos `try...except` genéricos que retornam exceções do sistema diretamente para o cliente, exemplo: 
    ```
        except Exception as e:
            return jsonify({"erro": str(e)}), 500  # ← expõe mensagem interna
    ```
    Um tratamento desse tipo poderia retornar algo como: **"erro": "no such table: produtos"** ou **"erro": "UNIQUE constraint failed: usuarios.email"**, detalhando schemas de banco.


### 4. Números Mágicos (LOW) - [Problema de code smell]
- **Arquivo**: `models.py`
- **Descrição**: Uso de valores fixos (10000, 5000, 1000) para lógica de negócio sem constantes nomeadas. Esses valores deveriam ser constantes no projeto. Valores arbitrários diretamente no código dificulta a alteração e clareza.

### 5. Uso de print para Logging (LOW) - [Problema de code smell/observabilidade]
- **Arquivo**: Todo o projeto.
- **Descrição**: O projeto inteiro utiliza a função `print()` para registrar logs de erro, criação de recursos e notificações em vez de módulo `logging`. Em um ambiente de produção, esta abordagem carece de metadados essenciais para observabilidade, como níveis de log (INFO, WARNING, ERROR), timestamps precisos e identificadores de contexto.


# Análise Manual: ecommerce-api-legacy (Node.js/Express)

## Problemas Identificados

### 1. Configurações Sensíveis Hardcoded (CRITICAL) - [Problema de segurança]
- **Arquivo**: `src/utils.js`
- **Descrição**: Chaves de API e senhas de banco de dados expostas diretamente no código. Temos: 
```  
    const config = {
        dbUser: "admin_master",
        dbPass: "senha_super_secreta_prod_123", 
        paymentGatewayKey: "pk_live_1234567890abcdef",
        smtpUser: "no-reply@fullcycle.com.br",
        port: 3000
    }
```
Da forma que está sendo utilizado, existe um risco muito grande de exposição das credenciais. Além disso, expõe chave do gateway diretamente no log.

### 2. Todo o fluxo da aplicação está em um único arquivo (MEDIUM) - [Problema de acoplamento / violação de SRP]
- **Arquivo**: `src/AppManager.js`
- **Descrição**: A classe `AppManager` centraliza múltiplas funções (DB, Rotas, Lógica). Não existe separação clara de responsabilidades. Isso dificulta manutenções e testes.

### 3. N+1 Queries no Relatório Financeiro (MEDIUM) - [Problema de performance]
- **Arquivo**: `src/AppManager.js` (`/api/admin/financial-report`)
- **Descrição**: Para cada curso é feita uma query de matrículas, e para
  cada matrícula são feitas mais duas queries (usuário e pagamento).
  Com volume real de dados, o número de queries cresce de forma
  proporcional a cursos × alunos. Isso pode levar a um sério problema de performance em produção.


### 4. Sistema de logging inadequado (LOW) - [Problema de observabilidade]
- **Arquivo**: `src/AppManager.js`
- **Descrição**: Uso extensivo de `console.log` para depuração no fluxo principal. Sem nível, sem timestamp, sem persistência de logs. Mesmo ponto observado no projeto `code-smells-project`, aqui agravado pela exposição de dados sensíveis nos logs.

### 5. Nomenclatura de variáveis abreviadas (LOW) - [Problema de code smell]
- **Arquivo**: `src/AppManager.js`
- **Descrição**: Uso de variáveis como `u`, `e`, `p`, `cid` e `cc` dificulta o entendimento do código sem uma análise profunda do contexto. Isso é um clássico problema de code smell.



# Análise Manual: task-manager-api (Python/Flask)

## Problemas Identificados

### 1. Credenciais SMTP Hardcoded (CRITICAL) - [Problema de segurança]
- **Arquivo**: `services/notification_service.py`
- **Descrição**: E-mail e senha de servidor Gmail expostos no código fonte. Se o repositório for acessado indevidamente, a conta de email fica comprometida (invasão, envio de spam/phishing). Deveria vir de variáveis de ambiente.

### 2. Lógica duplicada (MEDIUM) - [Problema de code smell]
- **Arquivos**: `routes/task_routes.py`, `routes/user_routes.py`, `report_routes.py`
- **Descrição**: Lógica de validação e estado de tarefas concentrada nas rotas, além do fato de estar duplicada. Exemplo:
```
if t.due_date < datetime.utcnow():
    if t.status != 'done' and t.status != 'cancelled':

```
Essa validação acima de repete em vários pontos do projeto. Poderia ser um único método de validação.
  
### 3. Mistura de domínios (MEDIUM) - [Problema de acoplamento]
- **Arquivo**: `routes/report_routes.py`
- **Descrição**: Nesse arquivo é feito o uso de `Blueprint`no `Flask` para agrupar rotas, porém esse agrupamento acumula dois domínios distintos. Exemplo: 
```
   # Domínio 1: Relatórios
    @report_bp.route('/reports/summary', methods=['GET'])
    def summary_report(): ...

    @report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
    def user_report(): ...

    # Domínio 2: CRUD de Categorias
    @report_bp.route('/categories', methods=['GET'])
    def get_categories(): ...

    @report_bp.route('/categories', methods=['POST'])
    def create_category(): ...

    @report_bp.route('/categories/<int:cat_id>', methods=['PUT'])
    def update_category(): ...

    @report_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
    def delete_category(): ...
```
Relatórios são operações de leitura e não modificam dados, enquanto isso, categorias são um recurso gerenciável (CRUD). Isso torna-se um problema porque quem faz manutenção de relatórios, precisa mexer no mesmo arquivo de quem faz manutenção de categorias. Além disso, dificulta aplicação de middlewares, exemplo: relatório para um perfil X ou categorias para um perfil Y.

### 4. Imports Não Utilizados (LOW) - [Problema de code smell]
- **Arquivo**: `app.py`, `task_routes.py`, `report_routes.py`, etc.
- **Descrição**: Muitos imports esquecidos em diversos arquivos do projeto.

### 5. Falta de Logs (LOW)
- **Arquivo**: `user_routes.py`
- **Descrição**: Identificado blocos de capturas de exceções implementados de sem a captura real do erro, com a cláusula `except:`, ao invés de `except Exception as e:` (ruim também, mas "menos pior"). Basicamente da forma que é feito está apenas retornando o erro genérico e não criando log de nada, deixando o debug totalmente no escuro.

---

# Construção da Skill

Para automatizar o processo de refatoração e revisão dos projetos legados, foram criadas duas Custom Skills integradas: `refactor-arch` (Refatoração Arquitetural) e `review-refactor` (Revisão Técnica). Abaixo estão detalhadas as decisões de design, estrutura e desafios enfrentados durante o desenvolvimento delas.

## Decisões de Design e Estrutura

As skills foram estruturadas seguindo a anatomia recomendada pela ferramenta de execução de agentes (organização em diretórios `.gemini/skills/` contendo o arquivo de orquestração `SKILL.md` e a pasta `references/` para arquivos auxiliares de documentação em Markdown):

1. **SKILL.md (O Maestro):** Contém a definição das fases obrigatórias de execução com prompts e gatilhos explícitos para o agente.
2. **References (Base de Conhecimento):**
   - `project-analysis.md`: Heurísticas de detecção passiva de stacks e mapeamento estrutural.
   - `antipatterns-catalog.md`: Catálogo unificado com regras de validação arquitetural e de segurança.
   - `audit-report-template.md`: Template estruturado para a Fase 2 (Auditoria).
   - `mvc-guidelines.md`: Definição estrita das camadas models, controllers e routes.
   - `refactoring-playbook.md`: Guia de transformações seguras com exemplos de antes/depois.

---

## Catálogo de Anti-patterns e Code Smells

O catálogo de detecção foi projetado contendo mais de 8 anti-patterns estratégicos divididos por criticidade, justificando sua inclusão pela gravidade técnica:

* **CRITICAL:**
  - *SQL Injection (AP-01):* Concatenação direta de queries (risco de destruição/vazamento de dados).
  - *Hardcoded Credentials (AP-02):* Segredos expostos diretamente no repositório (vulnerabilidade severa).
  - *Plaintext Passwords (AP-03):* Armazenamento sem hash seguro (vazamento total de acessos de clientes).
* **HIGH:**
  - *God Class / God Method (AP-04):* Lógica de negócio pesada, persistência e rotas aglomeradas em um único arquivo (AppManager ou app.py).
  - *Unprotected Routes (AP-06):* Falta de controle de acesso a rotas administrativas ou destrutivas.
  - *Missing Transactions (AP-07):* Operações de escrita composta executadas sem atomicidade/rollback.
* **MEDIUM:**
  - *N+1 Queries (AP-08):* Queries executadas dentro de loops que degradam drasticamente a performance.
  - *Verbose Error Disclosures (AP-10):* Exibição de exceções brutas ou schemas ao cliente.
* **LOW:**
  - *Magic Numbers (AP-12) & Console Logging (AP-13):* Ausência de constantes declarativas e observabilidade deficitária.

---

## Tecnologia Agnóstica (Independência de Stack)

Para garantir que a skill pudesse auditar e refatorar com sucesso tanto aplicações Python/Flask quanto Node.js/Express de forma dinâmica:
- **Heurísticas Abstratas:** Em vez de procurar arquivos fixos, o agente primeiro escaneia as dependências da aplicação (`package.json` vs `requirements.txt`) para determinar a linguagem principal.
- **Padrões Universais de Arquitetura:** O playbook de refatoração instrui o agente sobre como desacoplar responsabilidades em termos lógicos de MVC (Rotas → Lógica → Dados) em vez de comandos acoplados a linguagens específicas.
- **Boot Dinâmico:** A etapa de validação na Fase 3 descobre os comandos corretos de boot (ex: `node src/app.js` vs `python app.py`) baseando-se no arquivo de configuração do projeto.

---

## Desafios Encontrados e Resolução

1. **Gestão de Dependências na Instalação Fresh:**
   - *Desafio:* Bibliotecas adicionadas durante a refatoração (como `bcrypt` no Python ou `bcryptjs` no Node) causavam falha de boot ao rodar o projeto em uma nova instalação caso não estivessem declaradas nos manifestos.
   - *Solução:* Adicionamos o passo obrigatório `5.1 Verificar arquivo de dependências` na Phase 3 da skill, instruindo o agente a atualizar automaticamente o `requirements.txt` ou `package.json` antes de prosseguir com a validação operacional.
2. **Alertas de Linters / Variáveis Inutilizadas:**
   - *Desafio:* Variáveis temporárias de tratamento de exceções (como `except Exception as e:`) geravam alertas de variáveis declaradas mas não utilizadas no linter.
   - *Solução:* Configuramos o passo de limpeza e linter na Phase 3, instruindo o agente a varrer os diretórios com `pyflakes` ou `eslint` e ajustar a assinatura dos tratadores de exceção inutilizados.
3. **Revisão e Ajustes Baseados em Feedback**
   - *Desafio:* O feedback técnico apontou que a refatoração original falhava ao não implementar a validação de JWT assinado real (mantendo o mock de string de teste `fake-jwt-token-`) e por realizar exclusão direta de categorias sem validação de integridade referencial com tarefas associadas.
   - *Solução:* Reforçamos o playbook de refatoração com padrões seguros de validação de JWTs criptográficos assinados via `PyJWT` (Python) e `jsonwebtoken` (Node.js), além de regras de verificação preventiva antes de operações destrutivas. Atualizamos e re-executamos as fases em todos os projetos para garantir a resolução completa de todos os apontamentos da auditoria.
4. **Desvio de Camada em Middlewares (Bypass de Controller):**
   - *Desafio:* Identificou-se que decoradores e guards de rota (como `auth_helper.py`) realizavam consultas diretas ao banco de dados chamando os Models, contornando a camada de `Controller`. Isso quebrava o fluxo unidirecional e a integridade da arquitetura MVC.
   - *Solução:* Mapeamos o anti-pattern `AP-17` e o padrão de refatoração `PT-14` nas referências da skill, ensinando o agente a canalizar o acesso de banco em middlewares por meio dos respectivos controladores (ex: `usuario_controller.buscar_usuario`), garantindo o isolamento correto de responsabilidades.

---

# Resultados e Instruções de Execução


Esta seção apresenta os resultados obtidos com a refatoração arquitetural para o padrão MVC e as instruções de execução para cada projeto do repositório.

## Resultados

### Projeto 1: code-smells-project (Python / Flask)

- **Status da Validação:** CONFORME
- **Resumo dos Achados da Auditoria (Fase 2):**
  * **CRITICAL:** 4 | **HIGH:** 3 | **MEDIUM:** 4 | **LOW:** 4 (Total: 15 achados)
- **Checklist de Validação:**
  - [x] Estrutura física organizada em MVC (Models, Controllers, Routes) com importações unidirecionais corretas.
  - [x] Entry point (`app.py`) limpo, carregando configurações de arquivo e registrando Blueprints.
  - [x] Credenciais sensíveis e variáveis de ambiente isoladas em arquivo `.env`.
  - [x] Criptografia de senhas com bcrypt implementada de forma robusta e segura.
  - [x] Todas as queries parametrizadas (livre de SQL Injection).
  - [x] Transações atômicas com rollback em escritas compostas (criação de pedido e baixa de estoque).
  - [x] Otimização de queries N+1 usando JOINs e agrupamento em memória.
  - [x] Proteção das rotas com autenticação Bearer Token funcional.
  - [x] Tratamento de erros centralizado que impede exposição de stack traces de banco.
  - [x] Execução do linter `pyflakes` com zero avisos ou erros.
- **Observações sobre a Stack:** A refatoração no Flask foi efetuada mapeando a inicialização da aplicação no entrypoint [app.py] e utilizando `Blueprint`s para desacoplar as rotas. A persistência foi migrada do código embutido para funções estruturadas e seguras (utilizando queries parametrizadas `?` do driver `sqlite3`) nos arquivos da pasta [models/]. As regras de negócio foram encapsuladas na camada de [controllers/] e validações extras foram movidas para serviços auxiliares (como [services/notification_service.py]). O linter `pyflakes` foi executado e retornou status 0 (limpo de código morto ou imports órfãos).
- **Estrutura de Diretórios (Antes vs Depois):**

```text
Antes:
code-smells-project/
├── app.py           (Monolito contendo rotas e lógicas)
├── controllers.py   (Mistura de regras de negócio e validações)
├── models.py        (Banco de dados e queries SQL concatenadas)
└── database.py      (Inicialização do banco de dados)

Depois:
code-smells-project/
├── app.py (Entry point limpo e registro de Blueprints)
├── config.py (Configurações centralizadas com variáveis de ambiente)
├── database.py (Inicialização do banco de dados)
├── models/
│   ├── __init__.py
│   ├── pedido.py (Queries parametrizadas + Transação atômica)
│   ├── produto.py (Queries parametrizadas + Soft Delete)
│   └── usuario.py (Segurança e hash bcrypt de senhas)
├── controllers/
│   ├── __init__.py
│   ├── pedido_controller.py
│   ├── produto_controller.py
│   └── usuario_controller.py
├── routes/
│   ├── __init__.py
│   ├── admin_routes.py
│   ├── auth_helper.py (Validação e decorators de rota)
│   ├── pedido_routes.py
│   ├── produto_routes.py
│   ├── relatorio_routes.py
│   └── usuario_routes.py
└── services/
    ├── __init__.py
    └── notification_service.py (Envio de e-mail/SMS/push desacoplado)
```
- **Logs de Execução e Boot da Aplicação:**
  ```text
  2026-08-08 12:29:23,011 [INFO] ==================================================
  2026-08-08 12:29:23,011 [INFO] SERVIDOR INICIADO
  2026-08-08 12:29:23,011 [INFO] Rodando em http://localhost:5000
  2026-08-08 12:29:23,011 [INFO] ==================================================
   * Serving Flask app 'app'
   * Debug mode: on
  
  Iniciando testes de validação dos endpoints da API...
  GET / : Status 200
  GET /health : Status 200
  GET /produtos : Status 200
  GET /usuarios (sem token) : Status 401 (esperado 401)
  GET /usuarios (token admin) : Status 200
  GET /usuarios (token cliente) : Status 403 (esperado 403)
  POST /login : Status 200
  POST /pedidos (criar pedido) : Status 201
  GET /pedidos/usuario/2 : Status 200
  PUT /pedidos/2/status (admin) : Status 200
  PUT /pedidos/2/status (cliente) : Status 403 (esperado 403)
  GET /relatorios/vendas : Status 200
  
  ✓ Todos os endpoints validados com 100% de sucesso!
  ```

Checklist de validação disponível em:  [reports/review-project-1.md](./reports/review-project-1.md).
Prints com o funcionamento dos endpoints disponivel em [reports/project-1-prints](./reports/project-1-prints)


---

### Projeto 2: ecommerce-api-legacy (Node.js / Express)

- **Status da Validação:** CONFORME
- **Resumo dos Achados da Auditoria (Fase 2):**
  * **CRITICAL:** 3 | **HIGH:** 2 | **MEDIUM:** 2 | **LOW:** 2 (Total: 9 achados)
- **Checklist de Validação:**
  - [x] Estrutura física organizada em MVC (Models, Controllers, Routes, Middlewares) sob diretório `src/`.
  - [x] Eliminação completa do arquivo monolítico `AppManager.js` com fracionamento de responsabilidades.
  - [x] Credenciais expostas isoladas no `.env` e carregadas de forma segura.
  - [x] Criptografia de senhas utilizando hash `bcryptjs` no login e no seed do banco.
  - [x] Queries SQL parametrizadas com placeholders no driver SQLite para impedir SQL Injection.
  - [x] Transações atômicas aplicadas com rollback no fluxo de checkout da API.
  - [x] Otimização de queries N+1 no relatório financeiro usando LEFT JOIN.
  - [x] Middleware de proteção de rotas JWT funcional no Express.
  - [x] Tratamento centralizado de erros do Express sem vazamento de stack traces internos.
- **Observações sobre a Stack:** A refatoração no Node.js/Express eliminou a classe monolítica `AppManager.js` que centralizava banco, rotas e regras de negócio. Foi criada uma estrutura MVC limpa sob o diretório `src/`. As credenciais expostas foram movidas para variáveis de ambiente carregadas via `dotenv`. Consultas ao banco de dados SQLite foram parametrizadas para evitar injeções, e senhas de usuários foram criptografadas com `bcryptjs`.
- **Estrutura de Diretórios (Antes vs Depois):**

```text
Antes:
ecommerce-api-legacy/
├── src/
│   ├── app.js (Configuração crua do Express)
│   ├── AppManager.js (Monolito acumulando rotas, lógica e banco)
│   └── utils.js (Credenciais hardcoded)
└── package.json

Depois:
ecommerce-api-legacy/
├── src/
│   ├── app.js (Composition Root)
│   ├── config.js (Carregamento seguro de variáveis de ambiente)
│   ├── database.js (Conexão singleton com SQLite)
│   ├── controllers/
│   │   ├── checkout_controller.js
│   │   ├── report_controller.js
│   │   └── user_controller.js
│   ├── models/
│   │   ├── audit_log.js
│   │   ├── course.js
│   │   ├── enrollment.js
│   │   ├── payment.js
│   │   └── user.js
│   ├── routes/
│   │   ├── checkout_routes.js
│   │   ├── report_routes.js
│   │   └── user_routes.js
│   └── middlewares/
│       └── auth.js (Middleware de proteção de rotas com JWT)
├── package.json
└── .env (Isolamento de variáveis locais)
```
- **Logs de Execução e Boot da Aplicação:**
  ```text
  ◇ injected env (6) from .env
  Frankenstein LMS rodando na porta 3000...
  
  Query de teste (Relatório Financeiro Administrativo com JWT):
  GET /api/admin/financial-report -> Status 200
  [{"course":"Clean Architecture","revenue":997,"students":[{"student":"Leonan","paid":997}]},{"course":"Docker","revenue":0,"students":[]}]
  ```

Checklist de validação disponível em: [reports/review-project-2.md](./reports/review-project-2.md).

Prints com o funcionamento dos endpoints disponivel em [reports/project-2-prints](./reports/project-2-prints)

---

### Projeto 3: task-manager-api (Python / Flask + SQLAlchemy)

- **Status da Validação:** CONFORME
- **Resumo dos Achados da Auditoria (Fase 2):**
  * **CRITICAL:** 3 | **HIGH:** 3 | **MEDIUM:** 1 | **LOW:** 2 (Total: 9 achados)
- **Checklist de Validação:**
  - [x] Estrutura MVC organizada respeitando a separação entre rotas, controllers e models de dados.
  - [x] Entry point limpo delegando conexões ao SQLAlchemy e registrando os Blueprints.
  - [x] Mapeamento de segredos e credenciais de SMTP Gmail para variáveis de ambiente locais.
  - [x] Criptografia de senhas com `bcrypt` e ocultação do campo de senha no schema `to_dict()`.
  - [x] Queries executadas de forma segura e parametrizada pela API nativa do SQLAlchemy ORM.
  - [x] Paginação e carregamento adiantado (`joinedload`) em queries para mitigar loop N+1.
  - [x] Middleware `token_required` aplicado de forma funcional para acesso seguro a rotas administrativas.
  - [x] Tratamento de erros centralizado com capturing genérico de Exceptions no Flask.
  - [x] Limpeza e correção total de variáveis e imports inúteis sinalizados pelo `pyflakes`.
- **Observações sobre a Stack:** A refatoração organizou o projeto estruturado em camadas mas com acoplamentos e brechas de segurança. Mapeamos as credenciais SMTP do Gmail de hardcoded para variáveis de ambiente, isolamos a lógica de notificações em `services/notification_service.py` e implementamos paginação e controle de consultas N+1 via `joinedload` no SQLAlchemy.
- **Estrutura de Diretórios (Antes vs Depois):**

```text
Antes:
task-manager-api/
├── app.py
├── database.py
├── models/
│   └── (User, Task, Category acoplados com rotas)
├── routes/
│   ├── (Mistura de validações duplicadas e endpoints misturados)
│   └── report_routes.py (Misturando relatórios e categorias)
└── services/

Depois:
task-manager-api/
├── app.py (Inicialização do Flask + SQLAlchemy + Error handling)
├── config.py (Configuração de email, db e segredos de ambiente)
├── database.py (Instanciação segura do db)
├── models/
│   ├── category.py (Entidade de categorias)
│   ├── task.py (Entidade de tarefas com relacionamento)
│   └── user.py (Criptografia bcrypt e proteção de senha)
├── controllers/
│   ├── category_controller.py
│   ├── report_controller.py
│   ├── task_controller.py
│   └── user_controller.py (Desacoplamento e fluxo limpo)
├── routes/
│   ├── category_routes.py (CRUD de categorias isolado)
│   ├── report_routes.py (Relatórios de visualização seguros)
│   ├── task_routes.py (Operações de tarefas)
│   └── user_routes.py (Gerenciamento e login)
├── utils/
│   ├── auth.py (Middleware JWT decorator)
│   └── helpers.py (Tratamento de exceções e payloads)
└── services/
    └── notification_service.py (Isolamento seguro de envio de emails)
```
- **Logs de Execução e Boot da Aplicação:**
  ```text
   * Serving Flask app 'app'
   * Debug mode: on
  2026-08-08 12:48:36,972 [INFO] werkzeug: WARNING: This is a development server...
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
  
  Query de teste (Health Check público):
  GET /health -> Status 200
  {"status": "ok", "timestamp": "2026-08-08 12:48:46.548816"}
  ```

Checklist de validação disponível em: [reports/review-project-3.md](./reports/review-project-3.md).
Prints com o funcionamento dos endpoints disponivel em [reports/project-3-prints](./reports/project-3-prints)

---

## Como Executar

### Ferramenta Utilizada

Este projeto foi analisado e refatorado com a skill **`refactor-arch`** usando o **Antigravity CLI (Gemini)** — assistente de codificação por linha de comando desenvolvido pelo Google DeepMind que suporta **skills** customizadas para fluxos especializados.

> **Nota:** O enunciado do desafio menciona Claude Code como exemplo de ferramenta. Este repositório utiliza o **Antigravity CLI (Gemini)** como ferramenta equivalente. A skill `refactor-arch` e seus arquivos de referência estão em `.gemini/skills/refactor-arch/` dentro de cada projeto.

### Como executar a skill `refactor-arch`

A skill opera em **3 fases sequenciais**: Análise → Auditoria → Refatoração.

**Pré-requisito:** Antigravity CLI instalado e configurado com uma chave de API Gemini válida.

**Executar em qualquer projeto:**

```bash
# Entre no diretório do projeto desejado
cd code-smells-project       # ou ecommerce-api-legacy / task-manager-api

# Inicie o Antigravity CLI
agy

# No chat, execute o comando da skill
> execute skill refactor-arch no projeto @<nome-do-projeto>
```

O agente irá automaticamente:
- **Fase 1** — detectar stack, mapear arquitetura e imprimir o resumo
- **Fase 2** — varrer o código contra o catálogo de anti-patterns e gerar `../reports/audit-project-N.md`
- **⛔ Pausa obrigatória** — exibir o relatório e pedir confirmação antes de modificar qualquer arquivo
- **Fase 3** — reestruturar o projeto para MVC, validar boot e endpoints (após confirmação)

**Confirmar a Fase 3 quando solicitado:**

```
Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
> y
```

---

### 1. code-smells-project (Python / Flask)

#### Instalação e Inicialização:
```bash
cd code-smells-project
# Cria e ativa o ambiente virtual
python3 -m venv venv
source venv/bin/activate
# Instala as dependências
pip install -r requirements.txt
# Configura o ambiente (.env)
cp .env.example .env
# Executa a aplicação
python app.py
```

#### Testando Endpoints Protegidos:
As rotas de relatórios, pedidos e listagem de usuários requerem autenticação por Token Bearer.
- **Obter Token (Login):**
  Envie uma requisição POST para `/login`:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"email": "admin@loja.com", "senha": "admin123"}' http://localhost:5000/login
  ```
  O retorno conterá os dados do usuário e o token JWT real assinado no campo `token`.
  
- **Consultar Usuários (Apenas Admin):**
  Use o cabeçalho `Authorization: Bearer <token>` com o token JWT retornado no login:
  ```bash
  curl -H "Authorization: Bearer <token_jwt>" http://localhost:5000/usuarios
  ```
  *(Se utilizar o token de um cliente comum, o acesso será negado com erro 403).*

- **Criar Pedido (Qualquer Usuário Autenticado):**
  ```bash
  curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <token_jwt>" -d '{"usuario_id": 2, "itens": [{"produto_id": 1, "quantidade": 1}]}' http://localhost:5000/pedidos
  ```

---

### 2. ecommerce-api-legacy (Node.js / Express)

#### Instalação e Inicialização:
```bash
cd ecommerce-api-legacy
# Instala dependências
npm install
# Copia o template de variáveis de ambiente
cp .env.example .env
# Inicia a aplicação
npm start
```

#### Testando Endpoints Protegidos:
As rotas administrativas e de exclusão de usuários requerem cabeçalho HTTP de autorização.
- **Realizar login:**
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"email": "leonan@fullcycle.com.br", "password": "123"}' http://localhost:3000/api/login
  ```
- **Acessar relatório financeiro (Admin):**
  ```bash
  curl -H "Authorization: Bearer <token_jwt>" http://localhost:3000/api/admin/financial-report
  ```

---

### 3. task-manager-api (Python / Flask)

#### Instalação e Inicialização:
```bash
cd task-manager-api
# Cria e ativa venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Roda a inicialização e sementes do banco
python seed.py
# Inicializa o app
python app.py
```

#### Testando Endpoints Protegidos:
As rotas de relatórios exigem autenticação do usuário.
- **Login:**
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"email": "joao@email.com", "password": "1234"}' http://localhost:5000/login
  ```
- **Acessar Resumo de Tarefas (Admin):**
  ```bash
  curl -H "Authorization: Bearer <token_jwt>" http://localhost:5000/reports/summary
  ```
- **Listar Tasks:**
  ```bash
  curl -H "Authorization: Bearer <token_jwt>" http://localhost:5000/tasks
  ```
