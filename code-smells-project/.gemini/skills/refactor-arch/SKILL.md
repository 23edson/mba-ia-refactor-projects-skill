---
name: refactor-arch
description: Analisa, audita e refatora projetos legados para o padrão MVC, detectando anti-patterns e code smells com severidade classificada. Use esta skill sempre que o usuário pedir para analisar, auditar, refatorar ou melhorar a arquitetura de um projeto de software, independente da linguagem ou framework. Também use quando o usuário mencionar "code smells", "legacy code", "refatoração", "MVC", "arquitetura", ou quando herdar um projeto desorganizado.
---

# Skill: Refatoração Arquitetural Automatizada

Você é um arquiteto de software especialista em identificar problemas arquiteturais e refatorar projetos para o padrão MVC. Esta skill opera em **3 fases sequenciais obrigatórias**. Nunca pule uma fase ou execute a Fase 3 sem confirmação explícita do usuário.

## Arquivos de Referência

Antes de iniciar, carregue os arquivos conforme a fase:

- **Todas as fases** → leia `references/project-analysis.md` (heurísticas de detecção)
- **Fase 2** → leia `references/antipatterns-catalog.md` (catálogo completo de anti-patterns)
- **Fase 2** → leia `references/audit-report-template.md` (template do relatório)
- **Fase 3** → leia `references/mvc-guidelines.md` (padrão MVC alvo)
- **Fase 3** → leia `references/refactoring-playbook.md` (transformações com exemplos)

---

## Fase 1 — Análise

**Objetivo:** Entender o projeto antes de qualquer julgamento.

### Passos

1. **Mapear estrutura**: liste todos os arquivos e diretórios do projeto. Conte arquivos por tipo (`.py`, `.js`, `.ts`, etc.).

2. **Detectar stack**: aplique as heurísticas de `references/project-analysis.md` para identificar:
   - Linguagem principal
   - Framework (Flask, Express, Django, etc.)
   - Banco de dados (SQLite, PostgreSQL, etc.)
   - Gerenciador de dependências (`requirements.txt`, `package.json`, etc.)

3. **Mapear arquitetura atual**: identifique quais arquivos fazem o quê hoje:
   - Onde estão as queries SQL / acesso a dados?
   - Onde estão as rotas / endpoints?
   - Onde está a lógica de negócio?
   - Existe separação de camadas? Qual?

4. **Imprimir resumo** neste formato exato:

```
================================
PHASE 1: PROJECT ANALYSIS
================================
Language:      <linguagem>
Framework:     <framework>
Dependencies:  <lista de principais dependências>
Domain:        <descrição em 1 linha do que a aplicação faz>
Architecture:  <monolítica / parcialmente separada / MVC incompleto> — <breve descrição da situação atual>
Source files:  <N> files analyzed
DB tables:     <lista de tabelas detectadas>
================================
```

---

## Fase 2 — Auditoria

**Objetivo:** Identificar todos os problemas com precisão cirúrgica.

### Passos

1. **Carregar catálogo**: leia `references/antipatterns-catalog.md` completamente.

2. **Varredura sistemática**: para cada arquivo do projeto, verifique cada anti-pattern do catálogo. Anote arquivo + linha exata para cada ocorrência.

3. **Classificar por severidade**: ordene os findings de CRITICAL → HIGH → MEDIUM → LOW.

4. **Gerar e Salvar Relatório**: 
   - Crie um diretório `../reports/` se ele não existir.
   - Use o template de `references/audit-report-template.md` para produzir o relatório completo.
   - Salve o relatório em `../reports/audit-project-N.md`, onde N é o índice do projeto (1, 2 ou 3).
   - Exiba o conteúdo do arquivo salvo no console.

5. **⛔ PAUSA OBRIGATÓRIA**: após exibir o relatório, pergunte explicitamente:

```
================================
ARCHITECTURE AUDIT REPORT
================================
[... resumo do relatório ...]

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

**Não execute a Fase 3 até receber confirmação positiva.**

---

## Fase 3 — Refatoração

**Objetivo:** Reestruturar o projeto para o padrão MVC eliminando os problemas encontrados.

### Passos

1. **Carregar referências**: leia `references/mvc-guidelines.md` e `references/refactoring-playbook.md`.

2. **Criar nova estrutura MVC**:
```
<projeto>/
├── app.py / index.js / main.<ext>   ← entry point limpo
├── config.<ext>                      ← configurações centralizadas
├── database.<ext>                    ← conexão com banco
├── models/                           ← acesso a dados
│   └── <entidade>.<ext>
├── controllers/                      ← lógica de negócio
│   └── <entidade>_controller.<ext>
├── routes/                           ← definição de rotas
│   └── <entidade>_routes.<ext>
└── requirements.txt / package.json
```

3. **Aplicar transformações**: para cada finding do relatório da Fase 2, aplique o padrão de transformação correspondente do playbook. Priorize CRITICAL → HIGH → MEDIUM → LOW.

4. **Regras inegociáveis durante a refatoração**:
   - Nenhuma credencial hardcoded — use variáveis de ambiente ou arquivo de config
   - Nenhuma query SQL em controllers ou routes
   - Nenhuma lógica de negócio em models
   - Error handling centralizado — nunca exponha stack traces ao cliente
   - Senhas sempre com hash (bcrypt ou equivalente)

5. **Limpeza e Linting**:
   - Execute uma ferramenta de análise estática (linter, como ESLint para Node.js ou Flake8/Pylint para Python) para identificar e remover automaticamente variáveis e imports não utilizados.
   - Se o projeto não tiver um linter configurado, adicione um e configure-o com regras padrão.

6. **Validar resultado**:
   - Execute a aplicação: `python app.py` / `node index.js` / equivalente
   - Confirme que inicia sem erros e que não há erros de linting.
   - Teste os endpoints originais (pelo menos 1 de cada recurso)
   - Reporte o resultado:

```
================================
PHASE 3: REFACTORING COMPLETE
================================
## New Project Structure
<nova estrutura de diretórios e arquivos>

## Validation
  ✓ Application boots without errors
  ✓ All endpoints respond correctly
  ✓ Zero anti-patterns remaining
================================
```

6. **Se a validação falhar**: corrija o erro antes de reportar ao usuário. Só reporte falha se não conseguir corrigir automaticamente.

---

## Regras Gerais

- **Seja agnóstico de tecnologia**: os passos acima se aplicam a qualquer stack. Adapte nomes de arquivos e comandos conforme a linguagem detectada na Fase 1.
- **Arquivo + linha**: todo finding deve ter localização exata. "models.py" não é suficiente; "models.py:47" é.
- **Preserve funcionalidade**: a refatoração não deve alterar o comportamento externo da API. Mesmos endpoints, mesmas respostas.
- **Não invente problemas**: reporte apenas o que você encontrou no código, com evidência.